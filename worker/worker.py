import json
import pika
import time
from cnn.rede_neural import Cnn

print("Iniciando worker", flush=True)


cnn = Cnn('models/best_model (1).keras') 

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue='cnn_queue', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    image_path = data['image_path']
    
    print(f" [x] Processando imagem: {image_path}", flush=True)
    
    # executa a inferência da rede neural
    resultado = cnn.predict_image(image_path)
    print(f" [x] Resultado obtido: {resultado}", flush=True)

    # se a api pedir alguma resposta
    if properties.reply_to:
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps({"resultado": resultado})
        )
    
    # confirma para o rabbit que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='cnn_queue',
    on_message_callback=callback,
    auto_ack=False # importante para garantir que nenhuma imagem suma se o worker cair
)

print("Aguardando mensagens")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Parando worker")
    connection.close()