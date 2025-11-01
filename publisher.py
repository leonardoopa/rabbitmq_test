import os 
import pika 
import json
from typing import Dict

from dotenv import load_dotenv
load_dotenv()

class RabbitMQPublisher:
    def __init__(self):
        self.__host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASSWORD")
        self.__channel = self.__create_channel()
        self.__exchange = "data_exchange"
        self.__routing_key = ""

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username, 
                password=self.__password
            ),
        )
        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel


    def send_message(self, body: Dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )



rabbitmq_publisher = RabbitMQPublisher()
rabbitmq_publisher.send_message({"message": "Ola!"})