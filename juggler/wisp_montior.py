

class WispMonitor:
    _response = None

    def __init__(self, call_queue_name="wisp", receive_queue_name="detonate") :
        self._call_queue_name = call_queue_name
        self._receive_queue_name = receive_queue_name

    def on_response(self, channel, method, properties, body):
        """
        Callback for request to wisp.
        """
        if self.corr_id == properties.correlation_id:
            self._response = body

    def call(self, body, unique_id=None):
        """
        Pass json formatted request to wisp, format is discussed at
        "https://github.com/hoonkim/rune/issues/10".

        Args:
            body(str): Json formatted message.
            unique_id(str): unique id.

        Returns:
            the result of request.

        """
        # @TODO To implement WispMonitor call.
        return None
