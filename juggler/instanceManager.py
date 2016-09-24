from instanceMonitor import Monitor
from wisp_monitor import WispMonitor
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
        print("Function Object created")

    def __init__(self, userName, projectName, functionData, parameters) :
        print("\n\nFunction Object Created")
        self.wisp_monitor = WispMonitor()

        functionData = json.loads(functionData)

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
    def ResponseFunctionCall (self, result, uId):
        print("uid :" + uId)
        print("function result :" + str(result))
        #send Result
        #Result have to contain the system resource info

        #send instance monitor info
        self.instanceMonitor.GetSystemState()
        self.instanceMonitor.DetailState()

        print('[[ resource state ]] ')
        print('--stuck--')
        print(self.instanceMonitor.stuck)

        print('--running--')
        print(self.instanceMonitor.running)

        print('--sleeping--')
        print(self.instanceMonitor.sleeping)

        
        #put the data
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
        jsondata = json.dumps({"user":self.userName,"project":self.projectName,"function":self.functionPath, "prams":self.parameters})
        print("send "+jsondata)

        #crawl function source        


        #call the function
        self.wisp_monitor.call(jsondata,  self.uFid , self.ResponseFunctionCall)

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
        print("instanceManager created")
        self.instanceMonitor = Monitor()
    def RunManager(self):
        print("Instance Manage is activated")
        
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
        user = self.jsonRequest["user"][0]
        project = self.jsonRequest["project"][0]
        functionObject = self.jsonRequest["function_object"][0]

        params = self.jsonRequest["params"][0]
        

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









