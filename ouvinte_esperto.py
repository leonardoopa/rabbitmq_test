import os 
import pika 
import sys  

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 1. Garantir que o Sorteador 'direct' existe
channel.exchange_declare(exchange='sorteador_direto', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]

if not severities:
    # Se não digitar nada, ele não vai receber nada!
    sys.stderr.write("Uso: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    # 2. Ligar a fila temporária ao Sorteador 'direct' com a etiqueta (routing_key)
    channel.queue_bind(
        exchange='sorteador_direto', 
        queue=queue_name, 
        routing_key=severity
    )

print(f" [*] Ouvinte esperando por etiquetas: {severities}. CTRL+C para sair.")

# 5. O que fazer quando o brinquedo chegar
def o_que_fazer_quando_chegar_o_brinquedo(ch, method, properties, body):
    # Mostra a etiqueta (routing_key) e a mensagem (body)
    print(f" [x] Recebi etiqueta '{method.routing_key}': {body.decode()}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=o_que_fazer_quando_chegar_o_brinquedo,
    auto_ack=False
)

channel.start_consuming()