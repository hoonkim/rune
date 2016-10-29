#impl your class for connection with NOVA API 
import sys

class NovaConnector:
    __flavorList = None
    __instanceList = None
    def __init__(self):
        self.__flavorList = {}
        #append flavorList when initialize

        self.__instanceList = {}
        #append instanceList when initialze

        print (sys._getframe().f_code.co_name)
    
    def getInstanceList(self):
        print (sys._getframe().f_code.co_name)
        return self.__instanceList

    def getInstance(self, uuid):
        print (sys._getframe().f_code.co_name)

        for item in self.__instanceList:
            if(item.getUUID() == uuid):
                return item

        return None

    def addInstance(self, name, flavor):
        print (sys._getframe().f_code.co_name)

    def deleteInstance(self, uuid):
        print (sys._getframe().f_code.co_name)

    def getFlavorList(self):
        print (sys._getframe().f_code.co_name)
        return self.__flavorList

    def getFlavor(self, id):
        print (sys._getframe().f_code.co_name)

        for item in self.__flavorList:
            if(item.getUUID() == uuid):
                return item

        return None



class RuneInstance:
    WAIT_TO_CREATE = 0
    INITIALIZING = 1
    SUSPEND = 1
    RUNNING = 2

    __uuid = None
    __name = None
    __address = None
    __core = None
    __memory = None
    __storage = None
    __state = None
    
    def __init__(self, name, flavor, state):
        self.__name = name
        self.__core = flavor["core"]
        self.__memory = flavor["memory"]
        self.__storage = flavor["storage"]

        self.__state = state

    def setUUID(self, uuid):
        self.__uuid = uuid

    def setAddress(self, addr):
        self.__address = addr

    def getUUID(self):
        return self.__uuid

    def getAddress(self):
        return self.__address

    def getInstance(self):
        retData = {}
        retData["uuid"] = self.__uuid
        retData["name"] = self.__name
        retData["core"] = self.__core
        retData["address"] = self.__address
        retData["memory"] = self.__memory
        retData["storage"] = self.__storage

        return retData

    def __str__(self):
        return str(self.getInstance())

class RuneFlavor:
    __uuid = None
    __name = None
    __core = None
    __memory = None
    __storage = None

    def init(self, uuid, name, addr, core, memory, storage):
        self.__uuid = uuid
        self.__name = name
        self.__core = core
        self.__memory = memory
        self.__storage = storage

    def getUUID(self):
        return self.__uid

    def getFlavor(self):
        retData = {}
        retData["uuid"] = self.__uuid
        retData["name"] = self.__name
        retData["core"] = self.__core
        retData["memory"] = self.__memory
        retData["storage"] = self.__storage

        return retData

    def __str__(self):
        return str(self.getFlavor())
