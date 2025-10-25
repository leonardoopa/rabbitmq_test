import pika
from dotenv import load_dotenv
import os


load_dotenv()

rabbitmq_user = os.getenv("RABBITMQ_USER")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD")


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__queue = "data_queue"
        self.__port = 5672
        self.__callback = callback
        self.__username = rabbitmq_user
        self.__password = rabbitmq_password

        self.__connection = None
        self.__channel = self.__create_channel()

    def __create_channel(self):
        parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username, password=self.__password
            ),
        )

        self.__connection = pika.BlockingConnection(parameters)

        channel = self.__connection.channel()

        channel.queue_declare(queue=self.__queue, durable=True)

        channel.basic_consume(
            queue=self.__queue, auto_ack=True, on_message_callback=self.__callback
        )

        return channel

    def start_consuming(self):
        print(
            f"[*] Aguardando mensagens na fila: {self.__queue}. Pressione CTRL+C para sair."
        )
        try:
            self.__channel.start_consuming()
        except KeyboardInterrupt:
            print("Consumo interrompido.")
            self.stop_consuming()

    def stop_consuming(self):
        if self.__connection and self.__connection.is_open:
            self.__connection.close()
            print("Conexão com RabbitMQ fechada.")


def minha_callback(ch, method, properties, body):
    print(f" [x] Mensagem recebida: {body.decode()}")


if __name__ == "__main__":
    rabbitmq_consumer = RabbitMQConsumer(callback=minha_callback)
    rabbitmq_consumer.start_consuming()
