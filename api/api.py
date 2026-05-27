import pika
import time
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import uuid
from pydantic import BaseModel
from typing import Optional
import shutil
import cnn.rede_neural as rn
from typing import List
app = FastAPI(title= "TaskAPI", description="API para gerenciamento de tarefas", version="1.0.0")


# credenciais de acesso
credentials = pika.PlainCredentials('admin', 'admin')

# modelo de dados para a tarefa
class Task(BaseModel):
    task_id: str
    payload: dict
    priority: Optional[int] = 0

# função para conectar e enviar ao RabbitMQ
def publish_to_queue(task: Task):
    # conectar ao RabbitMQ (nome do servidor no docker-compose.yml)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials))

    channel = connection.channel()

    # garante que a fila existe
    channel.queue_declare(queue='tasks', durable=True)
    # publica a mensagem na fila
    message = json.dumps(task.dict())

    channel.basic_publish(
        exchange="",
        routing_key='tasks',
        body=message,
        properties= pika.BasicProperties(delivery_mode=2, priority= task.priority)  # torna a mensagem persistente
    )
    connection.close()

@app.post("/tasks/")
async def create_task(task: Task):
    try:
        publish_to_queue(task)
        return {"status": "enqueued!", "task_id": task.task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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

    # Cria uma fila de resposta única para este lote
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    predictions_received = []
    expected_responses = len(files)
    correlation_ids = set()

    def on_response(ch, method, props, body):
        if props.correlation_id in correlation_ids:
            predictions_received.append(json.loads(body))
            channel.basic_ack(delivery_tag=method.delivery_tag)
            # Se já recebemos todas as respostas do lote, para de consumir
            if len(predictions_received) == expected_responses:
                channel.stop_consuming()

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=False)

    # Envia todas as imagens para a fila (os workers vão dividi-las entre si!)
    for file in files:
        filename = f'{uuid.uuid4()}.jpg'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

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

    # Aguarda todas as respostas voltarem dos workers
    start_time = time.time()
    while len(predictions_received) < expected_responses:
        connection.process_data_events(time_limit=1)
        if time.time() - start_time > 45: # Timeout um pouco maior para o lote
            connection.close()
            raise HTTPException(status_code=504, detail="Timeout processando lote de imagens")

    connection.close()
    
    return {
        'message': f'{expected_responses} imagens processadas com sucesso',
        'predictions': predictions_received
    }