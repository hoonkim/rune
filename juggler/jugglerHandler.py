from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from jugglerRequest import RuneRequest
from instanceManager import *

import json
import threading
import urllib


class RuneHttpHandler(BaseHTTPRequestHandler):
    instManager = None

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

        print("RECV POST DATA:", post_data)

        #run instance manager
        self.instManager = InstanceManager()
        self.instManager.RunManager()
        self.instManager.ReceiveRequest(json.dumps(post_data))
 
        # reponse
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        self.wfile.write(bytes("RECEIVED : ","utf-8"))
        self.wfile.write(str(post_data).encode("utf-8"))

        return str(post_data)        

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


if __name__ == "__main__":
    #create server
    PORT = 8000
    server = ThreadedHTTPServer(('127.0.0.1', PORT), RuneHttpHandler)
    print('Starting server, use <Ctrl-C> to stop')
    print('Waiting API call')
    server.serve_forever()


