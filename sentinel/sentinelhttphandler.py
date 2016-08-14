import sys
import json

#from time import sleep

sys.path.insert(0, '../runeHTTP')

from handler import *
from SentinelRequestHandler import *

class SentinelHttpHandler(RuneHttpHandler):
    __reqList = None

    def do_GET(self):
        info = self
        self.printClientInformation(info)
        self.pathParser(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.__reqList is None:
            self.__reqList = SentinelRequestList()

        requestName = self.path

    def do_POST(self):
        info = self
        self.printClientInformation(info)

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        print("POST DATA:", post_data)

        if self.__reqList is None:
            self.__reqList = SentinelRequestList()

        requestName = self.path

        if reqResult = self.__reqList().findRequest(requestName) is None:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            #json decode
            self.wfile.write(bytes("RECEIVED: ","utf-8"))
            reqData = json.loads(str(post_data).encode("utf-8"))

            self.wfile.write(str(reqResult(reqData)).encode("utf-8"))