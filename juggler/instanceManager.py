from instanceMonitor import Monitor
from wisp_monitor import WispMonitor
from time import strftime, localtime

import json
import psutil

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


    def __init__(self):
        print("\n\n[[[ Function Object created ]]]")

    def __init__(self, userName, projectName, functionData, parameters) :
        print("\n\n[[[  Function Object Created ]]]")
        self.wisp_monitor = WispMonitor()

        print("functionData", functionData)
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
    def ResponseFunctionCall (self, result, uId, instanceMonitor, executionTime):
        print("callback")
        print(result)
        print("uid :" + uId)
        print("function result :" + str(result))
        #send Result
        #Result have to contain the system resource info
        #send instance monitor info
        instanceMonitor.GetSystemState()
        instanceMonitor.DetailState()

        print('[[ resource state ]] ')
        print('--stuck--')
        print(self.instanceMonitor.stuck)

        print('--running--')
        print(self.instanceMonitor.running)

        print('--sleeping--')
        print(self.instanceMonitor.sleeping)
        
        #put the result data
        requestObject = RuneRequest()
        requestObject.insertRequest(result)
        req = RuneRequestSender(requestObject)
        ret = req.sendPOST("http://127.0.0.1:8000/test_post")

        if(ret) :
            print("GET REQUEST", ret.content)
            print("data sent successfully")
            return True
        else :
            print("request fail")
            return False

    #send function request to wisp 
    def SendFunctionRequest(self):
        timestamp = strftime("%Y/%H/%M/%S",localtime())

        functionObj = {"function_path":"/home/stack/juggler/rune/juggler/helloWorld.py", "timestamp":timestamp,"validation_required":"t"}

        jsondata = json.dumps({"user":self.userName,"project":self.projectName,"function_object":functionObj, "params":self.parameters})
       
        print("send "+jsondata)
       
        #crawl function source        

         

        #call the function
        ret = self.wisp_monitor.call(jsondata, self.uFid, self.ResponseFunctionCall)
        
        print("wisp_monitor called successfully")       
        return True

    def FunctionSourceCrawler(self):
        codePath = ""
        # address of code storage
        codeStorageLocation = ""
        
        #get function code from storage to this instance 

        #open functionFile from code Storage

        #write function File on code storage
        data = ""


        functionFile = open(uFid, 'w')
        print(str(uFid) + " function file created")


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

    def ReceiveRequest(self, jsonRequest) :
        
        #get data from Sentinel
        self.jsonRequest = json.loads(jsonRequest)
        print(self.jsonRequest)

        user = self.jsonRequest["user"]
        project = self.jsonRequest["project"]
        functionObject = self.jsonRequest["function_object"]

        params = self.jsonRequest["params"]
        

        print("\n[recv data ] \n user : " + str(user) + '\n projcet :  ' + str(project) + '\n func obj :  ' + str(functionObject) + '\n params :  ' + str(params))


        print("[[ func obj ]]")
        print(type(functionObject))
        # call functions based on receved data from sentinel
        f = Function(user, project, functionObject, params)
        
        #call function
        f.SendFunctionRequest()


 
        return True

if __name__ == "__main__":
    i = InstanceManager()
    i.RunManager()









