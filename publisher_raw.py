import pika 
import os
from dotenv import load_dotenv

load_dotenv()

rabbitmq_user = os.getenv("RABBITMQ_USER")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")
rabbitmq_host = os.getenv("RABBITMQ_HOST")
rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))


connection_parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=5672,
    credentials=pika.PlainCredentials(
        username=rabbitmq_user, password=rabbitmq_password
    ),
)

channel = pika.BlockingConnection(connection_parameters).channel()

channel.basic_publish(
    exchange="data_exchange",
    routing_key="data_queue",
    body="Ola!",
    properties=pika.BasicProperties(
        delivery_mode=2,  # Make message persistent
    )
)