import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.35.105'))
channel = connection.channel()

channel.queue_declare(queue='lambda')

channel.basic_publish(exchange='',
                      routing_key='lambda',
                      body='printcall')
print("lambda:print")
connection.close()
