import pika
import sys
from dotenv import load_dotenv
import os

load_dotenv()

rabbitmq_user = os.getenv("RABBITMQ_USER")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")


def minha_callback(ch, method, properties, body):
    print(f"Received {body}")


connection_parameters = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    credentials=pika.PlainCredentials(
        username=rabbitmq_user, password=rabbitmq_password
    ),
)

channel = pika.BlockingConnection(connection_parameters).channel()
channel.queue_declare(queue="data_queue", durable=True)

channel.basic_consume(
    queue="data_queue", auto_ack=True, on_message_callback=minha_callback
)

print("Listen RabbitMQ on data_queue, on Port 5672")
channel.start_consuming()
