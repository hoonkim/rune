import json

'''
#test data

data = '{ \
 "core" : 4, \
 "core_usage": [10, 20, 30, 40], \
 "memory_usage": 48, \
 "storage_usage": 70, \
 "network_send": 1087488, \
 "network_recv": 508123, \
 "uuid": "DF6328Q9326F" \
}'

data2 = '{ \
 "core" : 4, \
 "core_usage": [40, 20, 70, 40], \
 "memory_usage": 82, \
 "storage_usage": 95, \
 "network_send": 1087488, \
 "network_recv": 1508123, \
 "uuid": "DF6328Q9326E" \
}'

data3 = '{ \
 "core" : 4, \
 "core_usage": [90, 90, 90, 90], \
 "memory_usage": 100, \
 "storage_usage": 20, \
 "network_send": 3087488, \
 "network_recv": 4508123, \
 "uuid": "DF6328Q9326D" \
}'


a = json.loads(data);
b = json.loads(data2);
c = json.loads(data3);

inst1 = SentinelInstance(a)
inst2 = SentinelInstance(b)
inst3 = SentinelInstance(c)

print(inst1)
print(inst2)
print(inst3)

'''

class SentinelJobDistributer():
    __instanceList = None
    __currentMachineCount = 0

    def __init__(self):
        self.__instanceList = []

    def addInstance(self, instance):
        return self.__addInstance(instance)

    def __addInstance(self, instance):
        if not isinstance(instance, SentinelInstance):
            return False

        if self.__instnaceList == None:
            self.__instanceList = list()

        self.__instanceList.append(instance)
        return True

    def findInstance(self, uuid):
        return self.__findInstance(uuid)

    def __findInstance(self, uuid):
        for item in self.__instanceList:
            if(item.getUUID() == uuid):
                return item

        return None

    def removeInstance(self, uuid):
        return self.__removeInstance(uuid)

    def __removeInstance(self, uuid):
        targetInstance = self.findInstance(uuid)
        self.__instanceList.remove(targetInstance)
        return targetInstance

    def updateInstance(self, uuid, instanceData):
        targetInstance = self.findInstance(uuid)
        targetInstance.updateData(instanceData)
        return targetInstance


    def findUsableInstance(self):
        if len(self.__instanceList) == 0:
            return None

        #Apply Round robin 
        return self.__findRoundRobinInstance()

    def __findRoundRobinInstance(self):
        self.__currentMachineCount = self.__currentMachineCount+1

        if self.__currentMachineCount <= len(self.__instanceList):
            self.__currentMachineCount = 0

        ret = self.__currentMachineCount
        return ret


    def __findLeastCpuUsageInstance(self):
        #TBD
        ret = None
        return ret    


class SentinelInstance():
    __address = None
    __uuid = None
    __core = None
    __coreUsage = None
    __memoryUsage = None
    __storageUsage = None
    __networkSend = None
    __networkRecv = None

    def __init__(self, address, data):
        if address is None:
            raise ValueError("no address information")
        else:
            self.__address = address

        if "uuid" in list(data.keys()):
            self.__uuid = data["uuid"]
        else:
            raise ValueError("no uuid information")

        if "core" in list(data.keys()):
            self.__core = data["core"]
        else:
            print("no core information - default setting: 1")
            self.__core = 1

        if "core_usage" in list(data.keys()):
            self.__coreUsage = data["core_usage"]
        else:
            print("no core usage information - default setting: 0")
            coreUsage = []
            for i in range(0,self.__core):
                coreUsage[i] = 0
            self.__coreUsage = coreUsage

        if "memory_usage" in list(data.keys()):
            self.__memoryUsage = data["memory_usage"]
        else:
            print("no memory usage information - default setting: 1")
            self.__memoryUsage = 0

        if "storage_usage" in list(data.keys()):
            self.__memoryUsage = data["storage_usage"]
        else:
            print("no storage usage information - default setting: 1")
            self.__storageUsage = 0

        if "network_recv" in list(data.keys()):
            self.__networkRecv = data["network_recv"]
        else:
            print("no network receive information - default setting: 1")
            self.__networkRecv = 0

        if "network_send" in list(data.keys()):
            self.__networkSend = data["network_send"]
        else:
            print("no network send information - default setting: 1")
            self.__networkSend = 0

    def updateData(self, address, data):

        if not(address is None):
            self.__address = address

        if "uuid" in list(data.keys()):
            self.__uuid = data["uuid"]

        if "core" in list(data.keys()):
            self.__core = data["core"]

        if "core_usage" in list(data.keys()):
            self.__coreUsage = data["core_usage"]

        if "memory_usage" in list(data.keys()):
            self.__memoryUsage = data["memory_usage"]

        if "storage_usage" in list(data.keys()):
            self.__memoryUsage = data["storage_usage"]

        if "network_recv" in list(data.keys()):
            self.__networkRecv = data["network_recv"]

        if "network_send" in list(data.keys()):
            self.__networkSend = data["network_send"]

    def __str__(self):
        return "UUID: "+str(self.getUUID()) + " / Core: "  + str(self.__core) + " core - " + str(self.getCoreUsageTotal())  + " / memory: " + str(self.getMemoryUsage()) + " / storage: " + str(self.getStorageUsage()) +  " / network: " + str(self.getNetworkUsage())


    def getUUID(self):
        return self.__uuid

    def getCoreUsageTotal(self):
        sum = 0
        for i in range(0,self.__core):
            sum += self.__coreUsage[i]
        return int(round(sum  / self.__core))

    def getMemoryUsage(self):
        return self.__memoryUsage

    def getStorageUsage(self):
        return self.__storageUsage

    def getNetworkUsage(self):
        #down: 1Gps = 1000Mbps = 125MBps
        #up: 125MBPs / ? = ???

        return round(((self.__networkSend + self.__networkRecv) / (125*1024*1024))*100, 2)
