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


class SentinelInstance():
    __uuid = None
    __core = None
    __coreUsage = None
    __memoryUsage = None
    __storageUsage = None
    __networkSend = None
    __networkRecv = None

    def __init__(self, data):
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
            self.coreUsage = data["core_usage"]
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
            print("no storage usage information - default setting: 1")
            self.__networkRecv = 0

        if "network_send" in list(data.keys()):
            self.__networkRecv = data["network_recv"]
        else:
            print("no storage usage information - default setting: 1")
            self.__networkRecv = 0


    def getUUID(self):
        return self.__uuid

    def getCoreUsageTotal(self):
        sum = 0
        for i in range(0,self.__core):
            sum += self.__coreUsage[i]
        return int(round(sum  / self._core))

    def getMemoryUsage(self):
        return self.__memoryUsage

    def getStorageUsage(self):
        return self.__storageUsage

    def networkUsage(self):
        #down: 1Gps = 1000Mbps = 125MBps
        #up: 125MBPs / ? = ???

        return int(round((self.__networkSend + self.__networkRecv / 125*1024*1024)*100))


def SentinelJobDistributer():
    print("GO")
