import sys
import json

sys.path.insert(0, '../runeconnect')

#sentinel
from sentinelrequesthandler import *
from sentinelhttphandler import *

#runeconnect
from requestlist import *
from sentineljob import *
from request import *
from handler import *

class SentinelHttpHandler(RuneHttpHandler):
    __reqList = None
    __jobDistributer = None
    __requestSender = None

    def __initHandler(self):
        if self.__reqList is None:
            self.__reqList = SentinelRequestList()
            self.__initReceiver()

        if self.__jobDistributer is None:
            self.__jobDistributer = SentinelJobDistributer()
            self.__initJobDistributer()

        if self.__requestSender is None:
            self.__requestSender = RuneRequestSender()


    def __initReceiver(self):
        #add request function
        self.__reqList.addRequest("/invoke", self.__receiveFunctionCall)

    def __initJobDistributer(self):
        #add Job distributer init
        '''
        '''

    def do_GET(self):
        info = self
        self.printClientInformation(info)
        self.pathParser(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.__initHandler()

        requestName = self.path

        self.wfile.write(bytes("RECEIVED: ", "utf8"))

    def do_POST(self):
        info = self
        self.printClientInformation(info)

        length = int(self.headers['Content-Length'])

        if self.headers['Content-Type'] == 'application/json':
            post_data = self.decodeJsonRequest(self.rfile.read(length).decode('utf-8'))
        else:
            post_data = self.decodeDictRequest(self.rfile.read(length).decode('utf-8'))

        print("POST DATA:", post_data)

        self.__initHandler()

        requestName = self.path

        reqResult = self.__reqList.findRequest(requestName)

        if reqResult is None:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            #json decode
            self.wfile.write(bytes("RECEIVED: ","utf-8"))
            print("request info: " , type(post_data), str(post_data))
            #reqData = json.loads(str(post_data).encode("utf-8"))



            self.wfile.write(str(reqResult(post_data)).encode("utf-8"))

    def __receiveFunctionCall(self, requestData):
        '''
        for key in requestData.keys():
            for key2 in requestData[key]:
                print(key + ": " + key2)
        '''
        targetInstance = self.__jobDistributer.findUsableInstance()

        #temporary data for test
        functionObject = '{ "uFid" : 1, "function_path" : "/foo/bar/", "revision_seq" : 1, "validation_required" : true}'
        data = '{ "user" : "kim", "project" : "rune", "function" : '+functionObject+', "params" : [ "seoul", "kr", "nano" ] }'


        requestData = json.loads(data)

        requestObject = runeRequest()
        requestObject.insertRequest(data)

        __requestSender.sendPost("http://127.0.0.1:8000")
