import pika
import sys
import os

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="192.168.43.170", port="30072"),
)

channel = connection.channel()

channel.exchange_declare(exchange="analytics_nlp", exchange_type="topic")


result = channel.queue_declare(queue="", exclusive=True)

queue_name = result.method.queue

binding_keys = sys.argv[1:]

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange="analytics_nlp", queue=queue_name, routing_key=binding_key
    )

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)

channel.start_consuming()
