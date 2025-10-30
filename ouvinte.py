import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Sou um Ouvinte. Estou esperando mensagens. CTRL+C para sair.')


def o_que_fazer_quando_chegar_a_mensagem(ch, method, properties, body):
    print(f" [x] Eu ouvi: {body.decode()}")
    
channel.basic_consume(
    queue=queue_name,
    on_message_callback=o_que_fazer_quando_chegar_a_mensagem,
    auto_ack=True
)

channel.start_consuming()
