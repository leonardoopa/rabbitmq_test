import pika
import os 
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Olá Mundo!"

channel.basic_publish(
    exchange='logs',   # Nome da antena
    routing_key='',    # Não precisa de etiqueta, pois é 'fanout', etiquera que ele fala, seria pra uma exchange especifica
    body=message
)

print(f" [x] DJ falou: '{message}'")

connection.close()