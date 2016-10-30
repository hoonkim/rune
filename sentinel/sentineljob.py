import json
import requests

novaAddr = "127.0.0.1:9999/"

class SentinelJobDistributer():
    __instanceList = None
    __currentMachineCount = 0

    def __init__(self):
        self.__instanceList = []

    def addInstance(self, instance):
        return self.__addInstance(instance)

    def __addInstance(self, instance, flavor="m1.tiny"):
        #if not isinstance(instance, SentinelInstance):
        #    return False

        if self.__instanceList == None:
            self.__instanceList = list()

        #create vm
        cond = {"flavor": flavor}
        ret = requests.post(novaAddr+"instance", cond)
        retJson = ret.json()
        newInstance = SentinelInstance(retJson["address"], retJson)

        #add to vm list
        self.__instanceList.append(instance)

        return newInstance

    def addExistInstance(self, instance):
        if self.findInstance(instance.getUUID()) != None:
            return None

        return self.__addExistInstance(instance)

    def __addExistInstance(self, instance):
        if self.__instanceList == None:
            self.__instanceList = list()

        self.__instanceList.append(instance)

        print("instance count: ", len(self.__instanceList))

        return instance.getInfoTable()

    def findInstance(self, uuid):
        return self.__findInstance(uuid)

    def __findInstance(self, uuid):
        for item in self.__instanceList:
            if(item.getUUID() == uuid):
                return item

        return None

    def getInstanceList(self):
        return self.__getInstanceList()

    def __getInstanceList(self):
        retList = []
        for item in self.__instanceList:
            retList.append(item.getInfoTable())

        return retList


    def removeInstance(self, uuid):
        return self.__removeInstance(uuid)

    def __removeInstance(self, uuid):
        targetInstance = self.findInstance(uuid)
        result = requests.delete(novaAddr+"delete/"+uuid)
        self.__instanceList.remove(targetInstance)
        return result

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

        self.__currentMachineCount
        return self.__instanceList[self.__currentMachineCount]


    def __findLeastCpuUsageInstance(self):
        #TBD
        ret = None
        return ret    

class SentinelFlavor:
    idx = None
    name = None
    vcpu = None
    memory = None
    disk = None

    def __init__(self, idx, name, vcpu, memory, disk):
        self.id = idx
        self.name = name
        self.vcpu = vcpu
        self.memory = memory
        self.disk = disk


class SentinelInstance():
    __uuid = None
    __address = None
    __core = None
    __coreUsage = None
    __memoryTotal = None
    __memoryUsage = None
    __storageTotal = None
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
            coreUsage = [self.__core]
            for i in range(0,self.__core):
                coreUsage[i] = 0
            self.__coreUsage = coreUsage

        if "memory" in list(data.keys()):
            self.__memoryUsage = data["memory_total"]
        else:
            print("no memory total information - default setting: 1")
            self.__memoryTotal = 0

        if "memory_usage" in list(data.keys()):
            self.__memoryUsage = data["memory_usage"]
        else:
            print("no memory usage information - default setting: 1")
            self.__memoryUsage = 0

        if "storage" in list(data.keys()):
            self.__storageTotal = data["storage_total"]
        else:
            print("no storage total information - default setting: 1")
            self.__storageTotal = 0

        if "storage_usage" in list(data.keys()):
            self.__storageUsage = data["storage_usage"]
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
        print(data)

        data = json.loads(data)

        print(type(data))
        if not(address is None):
            self.__address = address

        if "uuid" in list(data.keys()):
            self.__uuid = data["uuid"]

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

    def getInfoTable(self):
        retObj = {}
        retObj["uuid"] = self.getUUID()
        retObj["address"] = self.getAddress()
        retObj["core"] = self.getCore()
        retObj["memory"] = self.getMemory()
        retObj["storage"] = self.getStorage()

        return retObj

    def getUUID(self):
        return self.__uuid

    def getAddress(self):
        return self.__address

    def getCore(self):
        return self.__core

    def getMemory(self):
        return self.__memoryTotal

    def getStorage(self):
        return self.__storageTotal

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
