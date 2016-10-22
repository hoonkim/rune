import json

import requests


class RequestBody:
    HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    HTTP_OK = 200

    def __init__(self, url):
        """
        Init with url to response
        Args:
            url: url to return result
        """

        self.url = url

    def send_response(self, body):
        """
        Send body back to ip.
        Args:
            body: json formatted string.

        Returns: if post result is 200

        """

        response_body = body if isinstance(body, str) else json.dumps(body)
        request = requests.post(self.url, headers=self.HEADERS, data=response_body)

        return request.status_code == self.HTTP_OK
