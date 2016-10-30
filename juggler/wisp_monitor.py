import json
import uuid
import pika
import threading


class WispMonitor:
    """
    WispMontior provides functions to controll wisp.
    """

    _corr_id = None

    _callbacks = dict()
    _consuming_thread = None

    def __init__(self, call_queue_name="wisp"):
        self._call_queue_name = call_queue_name
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._publish_channel = self._connection.channel()

        self._publish_channel.queue_declare(queue=self._call_queue_name)
        self._receive_channel = self._connection.channel()

        result = self._receive_channel.queue_declare(exclusive=True)
        self._receive_queue_name = result.method.queue

        self._consuming_thread = threading.Thread(target=self.start_consuming,
                                                  args=(self._receive_channel,
                                                        self._receive_queue_name,
                                                        self.on_response))
        self._consuming_thread.start()

    @staticmethod
    def start_consuming(channel, receive_queue_name, on_response):
        channel.basic_consume(on_response, no_ack=True, queue=receive_queue_name)
        channel.start_consuming()

    def on_response(self, channel, method, properties, body):
        """
        Callback for request to wisp.
        """
        parsed_body = json.loads(self.to_str(body))
        unique_id = parsed_body['uuid']

        # callback = self._callbacks.pop(unique_id)
        # callback(result, unique_id)

        self._callbacks[unique_id] = self.to_str(body)

    @staticmethod
    def to_str(bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        return value

    def call(self, body, unique_id):
        """
        Pass json formatted request to wisp, format is discussed at
        "https://github.com/hoonkim/rune/issues/10".

        Args:
            body(str): Json formatted message.
            unique_id(str): unique id.
            callback(function): call_back(result, unique_id)

        Returns:
            None

        """

        # Setting correlation id to identify request.
        if unique_id is None:
            self._corr_id = str(uuid.uuid4())
        else:
            self._corr_id = str(unique_id)

        if self._corr_id in self._callbacks.keys():
            return False

        # Publish to MQ from here.
        self._publish_channel.basic_publish(exchange='',
                                            routing_key=self._call_queue_name,
                                            properties=pika.BasicProperties(
                                                reply_to=self._receive_queue_name,
                                                correlation_id=self._corr_id,
                                            ), body=body)

        # Save callback in dictionary.

        self._callbacks[self._corr_id] = None

        while self._callbacks[self._corr_id] is None:
            pass

        return self._callbacks.pop(self._corr_id)

