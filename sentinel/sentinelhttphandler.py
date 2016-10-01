import sys
import json

sys.path.insert(0, '../runeconnect')
sys.path.insert(0, '../runebook')

#sentinel
from sentinelrequesthandler import *
from sentinelhttphandler import *

#runeconnect
from requestlist import *
from sentineljob import *
from request import *
from handler import *

from runebook import *

class SentinelHttpHandler(RuneHttpHandler):
    __reqList = None
    __jobDistributer = None
    __runebookConnect = None

    def __initHandler(self):
        if self.__runebookConnect is None:
            self.__runebookConnect = RuneBookConnect()
        if self.__reqList is None:
            self.__reqList = SentinelRequestList()
            self.__initReceiver()

        if self.__jobDistributer is None:
            self.__jobDistributer = SentinelJobDistributer()
            self.__initJobDistributer()

    def __initReceiver(self):
        #add request function

        #function call
        self.__reqList.addRequest("/invoke", self.__receiveFunctionCall)

        #runebook connect

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
            #print("request info: " , type(post_data), str(post_data))
            #reqData = json.loads(str(post_data).encode("utf-8"))

            self.wfile.write(str(reqResult(post_data)).encode("utf-8"))


    def __getUser(self,requestData):
        cond = requestData["cond"]

        ret = self.__runebookConnect.getUser(cond)
        return ret

    def __getUserList(self,requestData):
        start = requestData["start"] 
        count = requestData["count"]
        cond = requestData["cond"]

        ret = self.__runebookConnect.getUserList(start, cound, cond)
        return ret

    def __addUser(self, requestData):
        user = requestData["user"]
        runeUser = RuneUser(user["userEmail"], user["userPassword"])

        ret = self.__runebookConnect.setUser(runeUser)
        return ret

    def __setUser(self, requestData):
        '''
        TBD
        '''

    def __removeUser(self, requestData):
        '''
        TBD
        '''

    def __getProject(self,requestData):
        cond = requestData["cond"]

        ret = self.__runebookConnect.getProject(cond)
        return ret

    def __getProjectList(self,requestData):
        start = requestData["start"] 
        count = requestData["count"]
        cond = requestData["cond"]

        ret = self.__runebookConnect.getProjectList(start, cound, cond)
        return ret

    def __addProject(self, requestData):
        project = requestData["project"]
        runeProject = RuneProject(user["userId"], user["projectName"])

        ret = self.__runebookConnect.setProject(runeProject)
        return ret

    def __setProject(self, requestData):
        '''
        TBD
        '''

    def __removeProject(self, requestData):
        '''
        TBD
        '''

    def __getFunction(self,requestData):
        cond = requestData["cond"]

        ret = self.__runebookConnect.getFunction(cond)
        return ret

    def __getFunctionList(self,requestData):
        start = requestData["start"] 
        count = requestData["count"]
        cond = requestData["cond"]

        ret = self.__runebookConnect.getFunctionList(start, cound, cond)
        return ret

    def __addFunction(self, requestData):
        code = requestData["function"]
        runeCode = RuneCode(code["projectId"], code["code"])

        ret = self.__runebookConnect.setFunction(runeCode)
        return ret

    def __setFunction(self, requestData):
        '''
        TBD
        '''

    def __removeFunction(self, requestData):
        '''
        TBD
        '''




    def __receiveFunctionCall(self, requestData):
        '''
        for key in requestData.keys():
            for key2 in requestData[key]:
                print(key + ": " + key2)
        '''
        targetInstance = self.__jobDistributer.findUsableInstance()

        #temporary data for test
        functionObject = '{ "uFid" : 1, "function_path" : "/foo/bar/", "revision_seq" : 1, "validation_required" : true}'
        data = '{ "user" : "kim", "project" : "rune", "function_object" : '+functionObject+', "params" : [ "seoul", "kr", "nano" ] }'


        requestData = json.loads(data)

        requestObject = RuneRequest()
        requestObject.insertRequest(requestData)

        requestSender = RuneRequestSender(requestObject)

        requestSender.sendPOST("http://127.0.0.1:8000/test_post")
