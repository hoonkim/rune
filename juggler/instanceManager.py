from instanceMonitor import Monitor
from wisp_monitor import WispMonitor
from time import strftime, localtime, mktime

import sys
import json
import psutil
import datetime

sys.path.insert(0, '../runeconnect')
from request import *

class Function :
    userNmae = ""
    projectName = ""
    functionPath = ""
    parameters = None

    uFid = None
    revisionSeq = None
    validationRequired = False    

    port = 8000
    wisp_monitor = None
    call_queue_name = "wisp"
    receive_queue_name="detonate"


    def __init__(self, userName=None, projectName=None, functionData=None, parameters=None) :
        print("\n\n[[[  Function Object Created ]]]")
        self.wisp_monitor = WispMonitor(self.call_queue_name)
        
        print("functionData", functionData)
       
        if(userName is not None):
            self.uFid = functionData["uFid"]
            self.functionPath = functionData["function_path"]
            self.revisionSeq = functionData["revision_seq"]
            self.validationRequired = functionData["validation_required"]
            self.userName = userName
            self.projectName = projectName
            self.parameters = parameters

            print("[[ function call log ]]")
            print("function uid : " + str(self.uFid))
            print("function path : " + str(self.functionPath))
            print("revision sequence : " + str(self.revisionSeq))
            print("validation required : " + str(self.validationRequired))
    
    # this function send response to sentinel
    # THE CALLBACK
    def ResponseByFunctionCall (self, functionResult, uId, functionStartTime):
        print("_CALLBACK FUNCTION_")
        print("uid :" + str(uId))
        print("function result :" + str(functionResult))
        
        #send Result
        #Result have to contain the system resource info
        #send instance monitor info
        
        functionEndTime = localtime() 

        functionStartTime = mktime(functionStartTime)
        functionEndTime = mktime(functionEndTime)

        elapsedTime = functionEndTime - functionStartTime

        instanceMonitor = Monitor()
        instanceMonitor.GetSystemState()
       
        #default resource data
        # 1. CPU usage
        # 2. Memory usage
        # 3. I/O Status

        print(instanceMonitor)
        resultJson = json.dumps({"functionResult": functionResult, "instanceState":str(instanceMonitor),"elapsedtime" : elapsedTime})

        return resultJson

    #send function request to wisp 
    def SendFunctionRequest(self):
        functionStartTime = localtime()
        
        functionObject = {"function_path":"/home/stack/rune/juggler/ServerTime.py", "timestamp": strftime("%Y/%H/%M/%S",functionStartTime),"validation_required":self.validationRequired}
        #functionObject = {"function_path":self.functionPath,"timestamp":strftime("%Y/%H/%M/%S",functionStartTime),"validation_required":self.validationRequired}

        jsondata = json.dumps({"user":self.userName,"project":self.projectName,"function_object":functionObject, "params":self.parameters})
       
        print("send "+ jsondata)

        #crawl function source        
        callResult = None
        
        #call the function
        functionResult = self.wisp_monitor.call(jsondata, self.uFid)

        responseOfFunctionCall = self.ResponseByFunctionCall(functionResult, self.uFid, functionStartTime)
        
        print(responseOfFunctionCall)


        return responseOfFunctionCall

    def FunctionSourceCrawler(self):
        sourcePath = ""
        # address of code storage
        
        sourcePath = str("~/source/"+self.uFid+".py")
        #write file 
        if(self.validationRequired == 'T'):
            #get function code from storage to this instance 
            argument = json.dumps({"code_id":self.uFid})
            headers = {'Content-type': 'application/json'}
           
            functionObject = requests.post("http://127.0.0.1:8000/getFunction", json=argument, headers=headers)
            
            functionJson = functionObject.json()

            print(functionJson)
            functionCode = functionJson["code"]

            self.CodeFileWriter(functionCode, sourcePath)
        else :
            #no write
            print("request a function directly")
            
        return sourcePath

    def CodeFileWriter(self, code, sourcePath):
        #write file
        sourceFile = open(sourcePath,"wr")
        sourceFile.write(code)
        sourceFile.close()
        print("request a function after function file is created")



# main class of Juggler
class InstanceManager :
    instanceMonitor = None 
    jsonRequest = None
    jsonRespons = None


    def __init__(self) :
        print("\n\n[[[ instanceManager created ]]]")
        self.instanceMonitor = Monitor()
    def RunManager(self):
        print("\n\n[[[ Instance Manage is activated ]]]")
        
        #run monitor 

    def SendRequest(self):
        data = "SystemData"
        requestObject = RuneRequest()
        requestObject.insertRequest(data)
        req = RuneRequestSender(requestObject)
       
        #Send to Sentinel
        ret = req.sendPOST("http://127.0.0.1:8000/test_post")
        if(ret) :
            print("POST  REQUEST", ret.content)
            print("data sent successfully")
            return True
        else :
            print("request fail")
            return False
        return True

    def SendResponse(self):
        return True 

    def ReceiveResponse(self, jsonResponse):
        return True

    def ReceiveRequest(self, jsonRequest, handler) :
        
        #get function call from Sentinel

        self.jsonRequest = json.loads(jsonRequest)
        print(self.jsonRequest)

        user = self.jsonRequest["user"]
        project = self.jsonRequest["project"]
        functionObject = self.jsonRequest["function_object"]

        params = self.jsonRequest["params"]
        
        print("\n[recv data ] \n user : " + str(user) + '\n projcet :  ' + str(project) + '\n func obj :  ' + str(functionObject) + '\n params :  ' + str(params))

        print("[[ func obj ]]")
        print(type(functionObject))


        #call functions based on receved data from sentinel
        newFunction = Function(user, project, functionObject, params)
      
        #crawl function
        # newFunction.FunctionSourceCrawler()

        #call function
        jsonresult = newFunction.SendFunctionRequest()

        handler.send_response(200)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
       
        print(type(jsonresult))
        print(jsonresult)
        handler.wfile.write(jsonresult.encode("utf-8"))

        return True

if __name__ == "__main__":
    i = InstanceManager()
    i.RunManager()









