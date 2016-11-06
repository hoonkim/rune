import threading
from http.server import BaseHTTPRequestHandler

from novaconnector import *

sys.path.insert(0, '../runeconnect')
from requestlist import RuneRequestList
from request import *
from handler import *


class InstanceManagerServer(BaseHTTPRequestHandler):
    HTTP_OK = 200
    PAGE_NOT_FOUND = 404
    
    __reqList = None
    __novaConnector = None

    def __initHandler(self):
        if self.__reqList is None:
            self.__reqList = RuneRequestList()
            self.__initReceiver()

        if self.__novaConnector is None:
            self.__novaConnector = NovaConnector()

    def __initReceiver(self):
        #add request function

        #function call
        self.__reqList.addRequest("/invoke", self.__receiveFunctionCall)

        #runebook connect

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

        '''
        thread = threading.Thread(target=self._handle_request, args=(post_body,))
        thread.start()
        '''

        if reqResult is None:
            self.send_response(PAGE_NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.send_response(HTTP_OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            #json decode
            self.wfile.write(bytes("RECEIVED: ","utf-8"))
            #print("request info: " , type(post_data), str(post_data))
            #reqData = json.loads(str(post_data).encode("utf-8"))

            self.wfile.write(str(reqResult(post_data)).encode("utf-8"))

    def __getInstanceList(self, requestData):
        return self.__novaConnector.getInstanceList()

    def __getInstance(self, requestData):
        uuid = requestData["uuid"]
        return self.__novaConnector.getInstance(uuid)

    def __addInstance(self, requestData):
        name = requestData["name"]
        flavor = requestData["flavor"]
        return self.__novaConnector.addInstance(name, flavor)

    def __deleteInstance(self, requestData):
        uuid = requestData["uuid"]
        return self.__novaConnector.deleteInstance(uuid)

    def __getFlavorList(self, requestData):
        return self.__novaConnector.getFlavorList()

    def __getFlavor(self, requestData):
        uuid = requestData["uuid"]
        return self.__novaConnector.getFlavor(uuid)


'''
    @staticmethod
    def _handle_request(body):
        # TODO @seok0721 handle request here.
'''
