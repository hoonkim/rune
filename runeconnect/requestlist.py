class RuneRequestList:
    __requestList = {}

    def addRequest(self, requestName, requestFunction):
        if self.__requestList is None:
            self.__requestList = {}

        self.__requestList[requestName] = requestFunction

        return True

    def findRequest(self, requestName):
        if requestName in list(self.__requestList.keys()):
            return self.__requestList[requestName]

        return None