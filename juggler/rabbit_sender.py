from wisp_monitor import WispMonitor
import sys
import json
import pika
import json 

sys.path.append("../")

from runeHTTP.request import RuneRequestSender
from runeHTTP.request import RuneRequest

class FunctionCaller :
    port = 8000
    wisp_monitor = None
    call_queue_name="wisp"
    receive_queue_name="detonate"	
    def __init__ (self):
        self.wisp_monitor = WispMonitor()
        print("created")
    def ReceiveFunctionCall (self):
        #receive Function Call request JSON
        print ("start receive function call")	
    #this function will be executed on wisp monitor
    #and send result data to controller
    def ResponseFunctionCall (self, result, uId):
        print("uid :" + uId)
        print("function result :" + str(result))
        #send Result
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
    def SendFunctionCall (self,username, project, function, params ): 
        print ("start send function call")
        jsondata = json.dumps({"user":username,"project":project,"function":function, "prams":params})
        print("send "+jsondata)
        self.wisp_monitor.call(jsondata, ResponseFunctionCall)		
        return True
    def ReceiveFunctionResult(self):
        return True

