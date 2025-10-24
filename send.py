import pika

# 1. Conecta ao servidor RabbitMQ (no seu localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Declara a fila (você já tinha essa parte)
# Isso garante que a fila 'hello' exista. É idempotente.
channel.queue_declare(queue='hello')

# 3. Publica a mensagem
channel.basic_publish(exchange='',           # Exchange padrão (default)
                      routing_key='hello',  # O nome da fila para onde enviar
                      body='Ola, RabbitMQ!') # O conteúdo da mensagem

print(" [x] Enviado 'Ola, RabbitMQ!'")

# 4. Fecha a conexão (e garante que os buffers de rede sejam limpos)
connection.close()