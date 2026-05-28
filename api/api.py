import pika
import time
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from pydantic import BaseModel
from typing import Optional
import shutil
import cnn.rede_neural as rn
from typing import List
app = FastAPI(title= "TaskAPI", description="API para gerenciamento de tarefas", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# credenciais de acesso
credentials = pika.PlainCredentials('admin', 'admin')

# modelo de dados para a tarefa
class Task(BaseModel):
    task_id: str
    payload: dict
    priority: Optional[int] = 0

@app.get("/health")
def health_check():
    return {"status": "ok"}


UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.post('/predict')
async def predict(files: List[UploadFile] = File(...)):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='cnn_queue', durable=True)

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    predictions_received = []
    expected_responses = len(files)
    correlation_ids = set()
    file_paths = []  # Armazena os caminhos das imagens salvas

    def on_response(ch, method, props, body):
        if props.correlation_id in correlation_ids:
            predictions_received.append(json.loads(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if len(predictions_received) == expected_responses:
                ch.stop_consuming()

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=False)

    # Envia todas as imagens para a fila
    for file in files:
        filename = f'{uuid.uuid4()}.jpg'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(filepath)  # guarda o caminho para exclusão posterior

        corr_id = str(uuid.uuid4())
        correlation_ids.add(corr_id)

        message = {'image_path': filepath}
        channel.basic_publish(
            exchange='',
            routing_key='cnn_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                reply_to=callback_queue,
                correlation_id=corr_id
            )
        )

    # Aguarda todas as respostas
    start_time = time.time()
    try:
        while len(predictions_received) < expected_responses:
            connection.process_data_events(time_limit=1)
            if time.time() - start_time > 45:
                raise HTTPException(status_code=504, detail="Timeout processando lote de imagens")
    finally:
        # Exclui todos os arquivos locais, independentemente de sucesso ou falha
        for filepath in file_paths:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Erro ao deletar {filepath}: {e}")
        connection.close()

    return {
        'message': f'{expected_responses} imagens processadas com sucesso',
        'predictions': predictions_received
    }