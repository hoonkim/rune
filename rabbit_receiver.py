import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.35.105'))
channel = connection.channel()

channel.queue_declare(queue='lambda')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='lambda',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
