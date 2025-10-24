import sys, os
import pika
import time


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        print(f" [x] Recebido: {body.decode()}")

        # Simula o trabalho: cada '.' no corpo da mensagem
        # vale 1 segundo de trabalho.
        dot_count = body.count(b".")
        print(f" [ ] Trabalhando por {dot_count} segundos...")
        time.sleep(dot_count)

        print(" [x] Feito (Done)")

        # MUDANÇA 2: Confirmação Manual (Ack)
        # Avisa manualmente ao RabbitMQ que a mensagem foi processada
        # com sucesso. Só agora o Rabbit pode deletá-la da fila.
        # Se o worker morrer antes desta linha, a mensagem será
        # re-enviada para outro worker.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 4. Consumo da Fila
    # MUDANÇA 3: Removemos 'auto_ack=True'.
    # Agora as confirmações são manuais (feitas na linha 'ch.basic_ack' acima).
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

    # 5. Inicia o Consumo
    channel.start_consuming()


# Bloco para lidar com CTRL+C de forma limpa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrompido")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
