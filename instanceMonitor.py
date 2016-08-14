from runeHTTP.request import RuneRequest
from runeHTTP.request import RuneRequestSender
import json
import psutil
import uuid
import socket


class Monitor:
	cpu_count = 0
	cpu_percent = 0
	instance_address = None
	mem = None 
	disk_usage = None 
	disk_io = None 
	net_io = None
	address = None
	hostname = None
	def GetSystemState(self) :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',0))
		self.address = s.getsockname()[0]
		self.cpu_count = psutil.cpu_count()
		self.cpu_percent = psutil.cpu_percent(interval=1,percpu=True)
		self.mem = psutil.virtual_memory()
		self.disk_usage = psutil.disk_usage('/')
		self.disk_io = psutil.disk_io_counters()
		self.net_io = psutil.net_io_counters()
		self.hostname = socket.gethostname()

	def MakeJSON(self) :
		jsondata = json.dumps({"core":self.cpu_count, "core_usage":self.cpu_percent,"memory_usage": self.mem.percent, "storage_usage":self.disk_usage.percent ,"network_send":self.net_io.bytes_sent,"network_recv":self.net_io.bytes_recv, "hostname": self.hostname, "address":self.address})
		return jsondata


	def SendJSON(self, jsondata) :
		print("data sent successfully")
		requestObject = RuneRequest()
		data = json.loads(jsondata)
		requestObject.insertRequest(data)

		req = RuneRequestSender(requestObject)
		ret = req.sendPOST("http://127.0.0.1:8000/test_post")
		if(ret) :
			print("GET REQUEST", ret.content)
		else :
			print("request fail")
		return True





