from urllib.parse import urlparse, parse_qs
from  http.client import HTTPConnection
import requests
import sys
import json

class RuneRequest:
    name = None
    queries = None
    child = None

    def __init__(self, requestString=None):
        if(requestString != None):
            self.requestString = requestString
            ret = self.parseRequest(requestString)

            name = 'NA'
            queries = {}

            if ret == False:
                print("requestSTring Type error")

    def insertRequest(self, requestData):
        if not isinstance(requestData, dict):
            print(sys._getframe().f_code.co_name , "mismatch type - ", type(requestData), type(dict))
            return False

        self.queries = requestData
        return True

    def parseRequest(self, requestString):
        if(requestString.strip() == ''):
            return False

        parseResult = urlparse(requestString)
        self.name = parseResult.path
        self.queries = parse_qs(parseResult.query)

        return True

    def addChild(self, requestObject):
        if not isinstance(requestObject, type(self)):
            print(sys._getframe().f_code.co_name , "mismatch type - ", type(requestObject), type(self))
            return False

        self.child = requestObject
        return True


    def __str__(self):
        ret = '<name: ' + str(self.name) + ', queries: ' + str(self.queries)

        if(self.child != None):
            ret += ', child: ' + str(self.child)

        ret += '>'

        return ret

    def getQueryJson(self):
        return json.dumps(self.queries)



class RuneRequestSender:
    _requestObject = None

    def __init__(self, requestObject=None):
        if requestObject != None:
            self.setRequestObject(requestObject)

    def setRequestObject(self, requestObject):
        if not isinstance(requestObject, RuneRequest):
            print(sys._getframe().f_code.co_name , "mismatch type - ", type(requestObject), type(RuneRequest))
            return False

        self._requestObject = requestObject
        return True

    def sendGET(self, requestAddr):
        r = requests.get(requestAddr)
        return r

    def sendPOST(self, requestAddr):
        if(self._requestObject is None):
            print("no request object")
            return False

        #r = requests.post(requestAddr, self._requestObject.getQueryJson())
#        r = requests.post(requestAddr, self._requestObject.queries)
        r = requests.post(requestAddr, json=self._requestObject.queries)
    
        return r





