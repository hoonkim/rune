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

    @staticmethod
    def __initHandler():
        if SentinelHttpHandler.__runebookConnect is None:
            SentinelHttpHandler.__runebookConnect = RuneBookConnect(serverHost="175.126.112.130", userId="rune", userPw="fjsld89", userDb="rune_dev")
        if SentinelHttpHandler.__reqList is None:
            SentinelHttpHandler.__reqList = SentinelRequestList()
            SentinelHttpHandler.__initReceiver()

        if SentinelHttpHandler.__jobDistributer is None:
            SentinelHttpHandler.__jobDistributer = SentinelJobDistributer()
            SentinelHttpHandler.__initJobDistributer()

    @staticmethod
    def __initReceiver():
        #add request function

        #state manage
        SentinelHttpHandler.__reqList.addRequest("/updateServerState", SentinelHttpHandler.__updateServerState)

        #function call
        SentinelHttpHandler.__reqList.addRequest("/invoke", SentinelHttpHandler.__receiveFunctionCall)

        #db connect
        SentinelHttpHandler.__reqList.addRequest("/getAuth", SentinelHttpHandler.__loginProc)
        SentinelHttpHandler.__reqList.addRequest("/addUser", SentinelHttpHandler.__addUser)
        SentinelHttpHandler.__reqList.addRequest("/getProjectList", SentinelHttpHandler.__getProjectList)
        SentinelHttpHandler.__reqList.addRequest("/addProject", SentinelHttpHandler.__addProject)
        SentinelHttpHandler.__reqList.addRequest("/removeProject", SentinelHttpHandler.__removeProject)
        SentinelHttpHandler.__reqList.addRequest("/getFunction", SentinelHttpHandler.__getFunction)
        SentinelHttpHandler.__reqList.addRequest("/getFunctionList", SentinelHttpHandler.__getFunctionList)
        SentinelHttpHandler.__reqList.addRequest("/addFunction", SentinelHttpHandler.__addFunction)
        SentinelHttpHandler.__reqList.addRequest("/removeFunction", SentinelHttpHandler.__removeFunction)
        SentinelHttpHandler.__reqList.addRequest("/updateFunction", SentinelHttpHandler.__setFunction)
        SentinelHttpHandler.__reqList.addRequest("/addExistInstance", SentinelHttpHandler.__addExistInstance)    
        SentinelHttpHandler.__reqList.addRequest("/getInstanceList", SentinelHttpHandler.__getInstanceList)

        #runebook connect        

    @staticmethod
    def __initJobDistributer():
        #add Job distributer init
        '''
        '''
        #test machine - localhost(when finnish server implement, remove)
        testInstanceData = {}
        testInstanceData["uuid"] = "kingston"
        testInstance = SentinelInstance("127.0.0.1", testInstanceData)

        SentinelHttpHandler.__jobDistributer.addExistInstance(testInstance)

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

        print("Content-header", self.headers['Content-type'])

        if self.headers['Content-Type'] == 'application/json':
            post_data = self.decodeJsonRequest(self.rfile.read(length).decode('utf-8'))
        else:
            post_data = self.decodeDictRequest(self.rfile.read(length).decode('utf-8'))

        print("POST DATA:", post_data, type(post_data))

        self.__initHandler()

        requestName = self.path

        print("req name : " + requestName)
        print("req addr : " +self.address_string())
        reqResult = SentinelHttpHandler.__reqList.findRequest(requestName)

        if reqResult is None:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            #json decode
            #self.wfile.write(bytes("RECEIVED: ","utf-8"))
            #print("request info: " , type(post_data), str(post_data))
            #reqData = json.loads(str(post_data).encode("utf-8"))

            result = str(reqResult(self, post_data)).encode("utf-8")
            print(result)
            self.wfile.write(result)

    def __getUser(self,requestData):
        cond = {"useremail": requestData["email"], "userpw": requestData["password"]}

        ret = SentinelHttpHandler.__runebookConnect.getUser(cond)
        return ret

    def __loginProc(self, requestData):
        cond = {"useremail": requestData["email"], "userpw": requestData["password"]}

        result = SentinelHttpHandler.__runebookConnect.getUser(cond)

        if result is None or result is ():
            return None

        userInfo = result[0]

        if userInfo is () or userInfo is None:
            return None
        print("raw", str(userInfo), "dump", json.dumps(userInfo))

        return json.dumps(userInfo)

    def __getUserList(self,requestData):
        #not fixed
        start = requestData["start"] 
        count = requestData["count"]
        cond = requestData["cond"]

        ret = SentinelHttpHandler.__runebookConnect.getUserList(start, cound, cond)
        return json.dumps(ret)

    def __getInstanceList(self, requestData):
        ret = json.dumps(SentinelHttpHandler.__jobDistributer.getInstanceList())
        return ret

    def __addUser(self, requestData):
        #not fixed
        #user = requestData["user"]
        runeUser = RuneUser(requestData["email"], requestData["password"])
        ret = SentinelHttpHandler.__runebookConnect.setUser(runeUser)
        return json.dumps(ret)

    def __setUser(self, requestData):
        '''
        TBD
        '''

    def __removeUser(self, requestData):
        '''
        TBD
        '''

    def __getProject(self,requestData):
        #not fixed
        cond = requestData["cond"]

        ret = SentinelHttpHandler.__runebookConnect.getProject(cond)
        return json.dumps(ret)

    def __getProjectList(self,requestData):
        userId = requestData["user_id"]

        ret = SentinelHttpHandler.__runebookConnect.getProjectList(None, None, {"userid": userId})
        return json.dumps(ret)

    def __addProject(self, requestData):
        userId = requestData["user_id"]

        projectName = requestData["project_name"]

        if str(projectName).strip() == "":
            return None

        project = RuneProject(userId, projectName)

        ret = SentinelHttpHandler.__runebookConnect.setProject(project)
        return json.dumps(ret)

    def __setProject(self, requestData):
        '''
        TBD
        '''

    def __removeProject(self, requestData):
        userId =  requestData["user_id"];
        name = requestData["name"];
        ret = self.__runebookConnect.deleteProject(userId, name)
        return json.dumps(ret)


    def __getFunction(self,requestData):
        print("requestData", str(requestData), type(requestData))
        cond = {"id": requestData["code_id"]}

        ret = SentinelHttpHandler.__runebookConnect.getFunction(cond)
        return json.dumps(ret)

    def __getFunctionList(self,requestData):
        projectId = requestData["project_id"]
        cond = {"projectid": projectId}

        ret = SentinelHttpHandler.__runebookConnect.getFunctionList(None, None, cond)
        return json.dumps(ret)

    def __addFunction(self, requestData):
        projectId = requestData["project_id"]
        name = requestData["code_name"]
        code = requestData["code_area"]

        runeCode = RuneCode(projectId, name, code, None, None)

        ret = SentinelHttpHandler.__runebookConnect.setFunction(runeCode)

        return json.dumps(ret)

    def __addExistInstance(self, requestData):
        
        newInstanceData = {}
        newInstanceData["uuid"] = requestData["uuid"]
        newInstance = SentinelInstance(self.address_string(), newInstanceData)

        ret = SentinelHttpHandler.__jobDistributer.addExistInstance(newInstance) 
      
    
        return json.dumps(ret)

    def __setFunction(self, requestData):
        codeId = requestData["code_id"]
        projectId = requestData["project_id"]
        name = requestData["code_name"]
        code = requestData["code_area"]

        runeCode = RuneCode(projectId, name, code, None, codeId)

        ret = SentinelHttpHandler.__runebookConnect.updateFunction({"id":codeId}, runeCode)
        
        return json.dumps(ret)

    def __removeFunction(self, requestData):
        id =  requestData["id"];
        projectId =  requestData["project_id"];
        name = requestData["name"];
        ret = self.__runebookConnect.deleteFunction(id,projectId,name)
        return json.dumps(ret)
        TBD

    def __updateServerState(self, uuid, requestData):
        targetInstance = req.__jobDistributer.findInstance(uuid)
        reqAddr = targetInstance.getAddress() + "GetStatus"

        requests.get(reqAddr)

    def __receiveFunctionCall(self, requestData):
        '''
        for key in requestData.keys():
            for key2 in requestData[key]:
                print(key + ": " + key2)
        '''
        
        targetInstance = SentinelHttpHandler.__jobDistributer.findUsableInstance()

        print("targetInstance", str(targetInstance))

        '''
        # temporary data for test
        functionObject = '{ "uFid" : 1, "function_path" : "/foo/bar/", "revision_seq" : 1, "validation_required" : true}'
        data = '{ "user" : "kim", "project" : "rune", "function_object" : '+functionObject+', "params" : [ "www.google.com" ] }'
        requestData = json.loads(data)

        ret = requestSender.sendPOST("http://127.0.0.1:8000/test_post")
        '''

        #generate argument for pass to Juggler
        codeId = requestData["code_id"]
        cond = {"id": codeId}
        codeRow = SentinelHttpHandler.__runebookConnect.getFunction(cond)

        functionObject = {
            "uFid": codeRow[0],
            "validation_required": True,
            #deprecated arguments
            "function_path": "/foo/bar", 
            "revision_seq": 1,
        }
        
        print("functionobject", str(functionObject))

        data = {
            "user": requestData["user_id"],
            "project": requestData["project_id"],
            "function_object": functionObject,
            "params": requestData["params"]

        }

        requestObject = RuneRequest()
        requestObject.insertRequest(data)

        requestSender = RuneRequestSender(requestObject)

        #print(str(targetInstance), "http://" + targetInstance.getAddress() + ":8000/callFunction")

        ret = requestSender.sendPOST("http://" + targetInstance.getAddress() + ":8000/callFunction")

        #get json result 
        jsonResult = ret.json()

        instanceState = jsonResult["instanceState"]
        functionResult = jsonResult["functionResult"]

        targetInstance.updateData(targetInstance.getAddress(),instanceState )

        print("[[ instance State ]]")
        print(instanceState)
        print("[[ function Reseult ]]")
        print(functionResult)

        return functionResult
