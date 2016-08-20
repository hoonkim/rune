import uuid
import pika


class WispMonitor:
    _response = None
    _corr_id = None

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
        if self._corr_id == properties.correlation_id:
            self._response = body

    def call(self, body, unique_id, call_back):
        """
        Pass json formatted request to wisp, format is discussed at
        "https://github.com/hoonkim/rune/issues/10".

        Args:
            body(str): Json formatted message.
            unique_id(str): unique id.
            call_back(function): call_back(result, unique_id)

        Returns:
            None

        """
        self._response = None

        # Setting correlation id to identify request.
        if unique_id is None:
            self._corr_id = str(uuid.uuid4())
        else:
            self._corr_id = unique_id

        self._channel.basic_publish(exchange='',
                                    routing_key=self._call_queue_name,
                                    properties=pika.BasicProperties(
                                       reply_to=self._receive_queue_name,
                                       correlation_id=self._corr_id,
                                   ),
                                    body=body)
        while self.response is None:
            self._connection.process_data_events()

        return str(self._response, "utf-8")
