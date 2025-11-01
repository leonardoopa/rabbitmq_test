import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 1. Criar o Sorteador (Exchange) do tipo 'direct'
channel.exchange_declare(exchange='sorteador_direto', exchange_type='direct')
    
# 2. Pegar a "cor da etiqueta" (a routing_key)
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

# 3. Pegar a mensagem (o brinquedo)
message = ' '.join(sys.argv[2:]) or 'Olá Mundo!'

# 4. Enviar o brinquedo COM a etiqueta
channel.basic_publish(
    exchange='sorteador_direto', # O nome do Sorteador
    routing_key=severity,       # A ETIQUETA! (ex: 'erro')
    body=message
)

print(f" [x] DJ enviou um brinquedo com etiqueta '{severity}': '{message}'")
connection.close()