from wisp_monitor import WispMonitor
import pika
import json 


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
	def ResponseFunctionCall (self, result, uId):
		return None	

	def SendFunctionCall (self,username, project, function, params ): 
		print ("start send function call")
		jsondata = json.dumps({"user":username,"project":project,"function":function, "prams":params})
		print("send "+jsondata)
		self.wisp_monitor.call(jsondata, ResponseFunctionCall)		
		return True
	
	
	def ReceiveFunctionResult(self):
		return True

