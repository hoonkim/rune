import pika
from utils import *


class MessageListener:
    """Message Listener listening to message queue."""

    _channel = None
    _connection = None
    _call_queue_name = None

    def __init__(self, server_ip, call_queue_name):
        """
        Init with serverIP of MQ Server and required queue name.
        Args:
            server_ip: Rabbit MQ Server.
            call_queue_name: Queue name that listener will wait for.
        """
        _connection = pika.BlockingConnection(pika.ConnectionParameters(
            server_ip
        ))
        self._channel = _connection.channel()
        self._channel.queue_declare(queue=call_queue_name)
        self._call_queue_name = call_queue_name

    def __str__(self):
        return self._quene_name

    @staticmethod
    def callback(channel, method, properties, body):
        # The callback for message Queue.

        string_body = str(body, 'utf-8')
        mod = message_to_function(string_body)

        if mod is not None:
            # Module loaded successfully.
            result = mod.run()
            print("fuck : " + result)
            # Sending back result to MQ.
            channel.basic_publish(exchange='',
                                  routing_key=properties.reply_to,
                                  properties=pika.BasicProperties(
                                      correlation_id=properties.correlation_id
                                  ),
                                  body=str(result)
                                  )

        else:
            print("mod is None")

        channel.basic_ack(delivery_tag=method.delivery_tag)



    def listen(self):
        """
        Start Listening to MQ Server. Ctrl + C to Exit.

        """

        self._channel.basic_consume(MessageListener.callback, queue=self._call_queue_name)
        self._channel.start_consuming()




