from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from request import SentinelRequestInformation
import threading


class SentinelHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET REQUEST', self)

        info = self
        self.printClientInformation(info)
        self.pathParser(self.path)

    def do_POST(self):
        print('GET REQUEST', self)

        info = self
        self.printClientInformation(info)
        

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

        for data in test:
            parseResult =  SentinelRequestInformation(data)
            if( oldObject != None ):
                oldObject.addChild(parseResult)
            else:
                firstObject = parseResult
            oldObject = parseResult

        return firstObject


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""