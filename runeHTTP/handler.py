from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from request import RuneRequest
import threading
import urllib


class RuneHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET REQUEST', self)

        info = self
        self.printClientInformation(info)
        self.pathParser(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        print('POST REQUEST', self)

        info = self
        self.printClientInformation(info)

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        print("POST DATA:", post_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        self.wfile.write(bytes("RECEIVED: ","utf-8"))
        self.wfile.write(str(post_data).encode("utf-8"))
        

    def printClientInformation(self, info):
        print("client addr - ", info.client_address)
        print("command - ", info.command)
        print("request line - ", info.requestline)
        print("path - ", info.path)

    def pathParser(self, path):
        if path.endswith('/') == False :
            path += '/'
        
        splitResult = path.split('/')

        oldObject = None
        firstObject = None

        print(splitResult)

        for data in splitResult:
            if data == '':
                continue
            parseResult =  RuneRequest(data)
            if( oldObject != None ):
                oldObject.addChild(parseResult)
            else:
                firstObject = parseResult
            oldObject = parseResult

        return firstObject

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
