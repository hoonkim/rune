import json
import psutil

class Monitor:
	cpu_count = 0
	cpu_percent = 0
	mem = None 
	disk_usage = None 
	disk_io = None 
	net_io = None
	def __init__(self):
		self.cpu_count = 0
		cpu_percent = 0
	def GetSystemStatus(self) :
		print("resource monitor info send")
		self.cpu_count = psutil.cpu_count()
		self.cpu_percent = psutil.cpu_percent(interval=1,percpu=True)
		self.mem = psutil.virtual_memory()
		self.disk_usage = psutil.disk_usage('/')
		self.disk_io = psutil.disk_io_counters()
		self.net_io = psutil.net_io_counters()
	def MakeJSON(self) :
		jsondata = json.dumps({"cpu_cnt":self.cpu_count, "cpu_percent":self.cpu_percent,"memory": self.mem.percent, "disk_usage":self.disk_usage.percent ,"net_byte_sent":self.net_io.bytes_sent,"net_byte_recv":self.net_io.bytes_recv })
		print(jsondata)

mon = Monitor()
 
mon.GetSystemStatus()
mon.MakeJSON()
