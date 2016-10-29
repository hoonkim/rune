from io import StringIO

import pika
from utils import *


class MessageListener:
    """Message Listener listening to message queue."""

    _channel = None
    _connection = None
    _call_queue_name = None

    ORIGINAL_STDOUT = sys.stdout
    ORIGINAL_STDERR = sys.stderr

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
        self._stdout = StringIO()
        self._stderr = StringIO()

    def __str__(self):
        return self._quene_name

    def callback(self, channel, method, properties, body):
        # The callback for message Queue.

        string_body = str(body, 'utf-8')
        mod = message_to_function(string_body)
        uuid = str(properties.correlation_id)

        if mod is not None:
            # Module loaded successfully.

            # Start capturing stdout and stderr.
            self.out_capture_start()
            result = mod.run()
            stdout, stderr = self.out_capture_end()

            body = {
                "result": result,
                "uuid": uuid,
                "stdout": stdout,
                "stderr": stderr
            }

            # Sending back result to MQ.
            channel.basic_publish(exchange='',
                                  routing_key=properties.reply_to,
                                  properties=pika.BasicProperties(
                                      correlation_id=properties.correlation_id
                                  ),
                                  body=json.dumps(body)
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

    def out_capture_start(self):
        """
        Override stdout and stderr to StringIO so that we can now save any output stream from module.
        Returns:

        """
        self._stdout.truncate(0)
        self._stderr.truncate(0)

        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def out_capture_end(self):
        out_string = self._stdout.getvalue()
        err_string = self._stderr.getvalue()

        sys.stdout = self.ORIGINAL_STDOUT
        sys.stderr = self.ORIGINAL_STDERR

        return out_string, err_string
