import threading
from http.server import BaseHTTPRequestHandler

from request_body import RequestBody


class InstanceManagerServer(BaseHTTPRequestHandler):
    HTTP_OK = 200

    def do_POST(self):
        self.send_response(200)
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = str(self.rfile.read(content_len))

        ip = self.client_address[0]
        port = self.client_address[1]

        request = RequestBody("http://" + ip + ":" + port);
        thread = threading.Thread(target=self._handle_request, args=(post_body, request))
        thread.start()

    @staticmethod
    def _handle_request(body, request):
        # TODO @seok0721 handle request here.

        result = ""
        request.send_reponse(result)
