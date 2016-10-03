import json
import uuid
import pika


class WispMonitor:
    """
    WispMontior provides functions to controll wisp.
    """

    _corr_id = None

    _callbacks = dict()

    def __init__(self, call_queue_name="wisp"):
        self._call_queue_name = call_queue_name
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

        self._channel = self._connection.channel()

        # make exclusive queue.
        result = self._channel.queue_declare(exclusive=True)
        self._receive_queue_name = result.method.queue

        self._channel.basic_consume(self.on_response, no_ack=True,
                                    queue=self._receive_queue_name)

    def on_response(self, channel, method, properties, body):
        """
        Callback for request to wisp.
        """

        print("on Response")
        parsed_body = json.loads(body)
        result = parsed_body['result']
        unique_id = parsed_body['uuid']
        self._callbacks[unique_id](result, unique_id)

    def call(self, body, unique_id, callback):
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

        if unique_id in self._callbacks.keys():
            return False

        # Publish to MQ from here.
        self._channel.basic_publish(exchange='',
                                    routing_key=self._call_queue_name,
                                    properties=pika.BasicProperties(
                                       reply_to=self._receive_queue_name,
                                       correlation_id=self._corr_id,
                                    ), body=body)

        # Save callback in dictionary.
        self._callbacks[unique_id] = callback

        return True

