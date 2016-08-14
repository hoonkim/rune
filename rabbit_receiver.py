import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='wisp')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # parse body by JSON Parser

channel.basic_consume(callback,
                      queue='wisp',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
