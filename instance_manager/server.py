import threading
from http.server import BaseHTTPRequestHandler


class InstanceManagerServer(BaseHTTPRequestHandler):
    HTTP_OK = 200

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len).decode("utf-8")

        thread = threading.Thread(target=self._handle_request, args=(post_body,))
        thread.start()

    @staticmethod
    def _handle_request(body):
        # TODO @seok0721 handle request here.
