import pika
from utils import *


class MessageListener:
    """Message Listener listening to message queue."""

    _channel = None
    _connection = None
    _queue_name = None

    def __init__(self, server_ip, queue_name):
        """
        Init with serverIP of MQ Server and required queue name.
        Args:
            server_ip: Rabbit MQ Server.
            queue_name: Queue name that listener will wait for.
        """
        _connection = pika.BlockingConnection(pika.ConnectionParameters(
            server_ip
        ))
        self._channel = _connection.channel()
        self._channel.queue_declare(queue=queue_name)
        self._queue_name = queue_name

    def __str__(self):
        return self._quene_name

    @staticmethod
    def callback(channel, method, properties, body):
        # The callback for message Queue.
        mod = message_to_function(body)
        result = mod()

    def listen(self):
        """
        Start Listening to MQ Server. Ctrl + C to Exit.

        """
        self._channel.basic_consume(MessageListener.callback, queue=self._queue_name)
        self._channel.start_consuming()


