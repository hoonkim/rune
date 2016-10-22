import sys
import json
import psutil
import uuid
import socket

sys.path.append("../runeconnect")

from request import RuneRequestSender
from request import RuneRequest


class SystemState :
    address = None
    cpu_count = 0
    cpu_percent = 0
    mem = None
    disk_usage = None
    disk_io = None
    net_io = None
    hostname = None

    def __init__(self):
        self.GetSystemState()
         
    def GetSystemState(self):
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
    stateJsonData = None
    
    sleeping = {}
    running = {}
    stuck = {}
    def GetSystemState(self):
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
        stateJsonData = json.dumps({"core":self.cpu_count, "core_usage":self.cpu_percent,"memory_usage": self.mem.percent, "storage_usage":self.disk_usage.percent ,"network_send":self.net_io.bytes_sent,"network_recv":self.net_io.bytes_recv, "hostname": self.hostname, "address":self.address})
        return stateJsonData


    
    def SendJSON(self, jsondata) :
        requestObject = RuneRequest()
        data = json.loads(jsondata)
        requestObject.insertRequest(data)
        req = RuneRequestSender(requestObject)
        ret = req.sendPOST("http://127.0.0.1:8000/test_post")
        if(ret) :
            print("GET REQUEST", ret.content)
            print("data sent successfully")
            return True
        else :
            print("request fail")
            return False

    def DetailState(self):
        self.GetSystemState()
        state = self.MakeJSON()
        state = json.loads(state)		
        #cpu detail
        cputimes = psutil.cpu_times()
        state['user'] = cputimes.user
        state['system'] = cputimes.system
        state['idle'] = cputimes.idle
        #memory detail
        state['totalsize'] = self.mem.total
        state['usedsize'] = self.mem.used
        #i/o detail
        state['disk_read'] = self.disk_io.read_bytes
        state['dist_write'] = self.disk_io.write_bytes
        # network I/O already contained on default
        #process			
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'status', 'cpu_percent', 'threads'])
            except psutil.NoSuchProcess:
                pass
            else:
                pid = pinfo['pid']
                if 'sleeping' in pinfo['status']:
                    self.sleeping[pid] = pinfo
                if 'running' in pinfo['status']:
                    self.running[pid] = pinfo
                if 'stuck' in pinfo['status']:
                    self.stuck[pid] = pinfo

    def __str__(self):
        return self.MakeJSON()


if __name__ == "__main__":
    m = Monitor()
    m.GetSystemState()
    m.DetailState()
    print(m.sleeping)
    print(m.running)
    print(m.stuck) 
