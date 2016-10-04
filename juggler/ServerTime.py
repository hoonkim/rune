from http.client import HTTPConnection
from http.client import HTTPSConnection
from urllib.parse import urlparse


def wisp_callback(url):
    """
    This returns current server's time of given url.

    :param url: url. (e.g. www.example.com, http://www.example.com, https://www.example.com:8080/test)
    :return: Date and time or the server.
    """
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme or "http"
    port = parsed_url.port or (80 if protocol == "http" else 443)
    path = parsed_url.path or "/"
    if parsed_url.hostname:
        url = parsed_url.hostname
    else:
        path = "/"
        url = parsed_url.path
    request = "GET"

    conn = (HTTPConnection if protocol == "http" else HTTPSConnection)(url, port)
    conn.request(request, path)
    response = conn.getresponse()
    time = response.getheader("Date")

    return time
