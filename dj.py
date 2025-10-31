import pika
import os 
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Olá Mundo!"

channel.basic_publish(
    exchange='logs',   
    routing_key='',    # Não precisa de etiqueta, pois é 'fanout', nesse caso ele vai enviar para todas as filas, etiqueta que ele fala, seria pra uma exchange especifica
    body=message
)

print(f" [x] DJ falou: '{message}'")

connection.close()