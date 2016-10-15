#!/usr/bin/python3
import json
import sys

sys.path.insert(0, '../runeconnect')

from mysql import RuneMySQLConnector

class RuneUser:
    __id = None
    __userEmail = None
    __userPassword = None

    def __init__(self, email, password, id=None):
        if id != None:
            self.__id = id

        self.__userEmail = email
        self.__userPassword = password

    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getEmail(self):
        return self.__userEmail

    def getPassword(self):
        return self.__userPassword

class RuneProject:
    __id = None
    __userId = None
    __projectName = None


    def __init__(self, userId, projectName, id=None):
        if id != None:
            self.__id = id

        self.__userId = userId
        self.__projectName = projectName


    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getUserId(self):
        return self.__userId

    def getProjectName(self):
        return self.__projectName


class RuneCode:
    __id = None
    __projectId = None
    __name = None
    __code = None
    __lastUpdateTime = None

    def __init__(self, projectId, code, lastUpdateTime=None, id=None):

        if id != None:
            self.__id = id

        self.__projectId = projectId
        self.__code = code
        
        if lastUpdateTime != None:
            self.__lastUpdateTime = lastUpdateTime

    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getProjectId(self):
        return self.__projectId

    def getCode(self):
        return self.__code

    def setCode(self, code):
        code = self.__code

    def getLastUpdateTime(self):
        return self.__lastUpdateTime



class RuneBookConnect:
    __runeMysql = None

    def __init__(self, serverHost=None, serverPort=None, userId=None, userPw=None, userDb = None, userCharset = None):
        self.__runeMysql = RuneMySQLConnector(serverHost, serverPort, userId, userPw, userDb, userCharset)

    def __generateCondition(self, cond):
        conditionString = ""

        for k,v in cond.items():
            if v is None:
                continue
            if conditionString == "":
                if k == "userpw":
                    conditionString = " WHERE " + k + "= password(\"" + str(v) +"\")"
                else:
                    conditionString = " WHERE " + k + "= \"" + str(v) +"\""
            else:
                if k == "userpw":
                    conditionString += " AND " + k + "= password(\"" + str(v) +"\")"
                else:
                    conditionString += " AND " + k + "= \"" + str(v) +"\""

        return conditionString

    def getUser(self, cond=None):
        query  = "SELECT * FROM user ";

        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)
        
        query = query + conditionString

        print(query)

        result = self.__runeMysql.sendRawQuerySelect(query, 1)

        return result




    def getUserList(self, start=None, count=None, cond=None):
        query  = "SELECT * FROM user ";
        
        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)

        query = query + conditionString

        print(query)

        if start != None:
            query += " OFFSET = " + start
        
        if count is None:
            count = 0

        result = self.__runeMysql.sendRawQuerySelect(query, count)

        return result

        

    def setUser(self, user):
        query = "INSERT INTO user(useremail, userpw) VALUES(\""+user.getEmail()+"\",password(\""+user.getPassword()+"\"))"

        print(query)

        ret = self.__runeMysql.sendRawQueryInsert(query)

        return ret


    def updateUser(self, cond=None, User=None):
        '''
        '''
        #TBD


    def deleteUser(self, cond=None, User=None):
        '''
        '''
        #TBD


    def getProject(self, cond=None):
        query  = "SELECT * FROM project ";

        conditionString = ""
        print("condition: ", cond)
        if cond != None:
            conditionString = self.__generateCondition(cond)
        
        query = query + conditionString

        print(query)

        ret = self.__runeMysql.sendRawQuerySelect(query, 1)

        return ret

    def getProjectList(self, start=None, count=None, cond=None):
        query  = "SELECT * FROM project ";
        
        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)

        query = query + conditionString

        if start != None:
            query += " OFFSET = " + start

        if count is None:
            count = 0

        print(query)
        
        ret = self.__runeMysql.sendRawQuerySelect(query, count)

        return ret

    def setProject(self, project):
        query = "INSERT INTO project(userid, name) VALUES(\""+str(project.getUserId())+"\",\""+project.getProjectName()+"\")"

        print(query)

        ret = self.__runeMysql.sendRawQueryInsert(query)

        return ret

    def updateProject(self, cond=None, Project=None):
        '''
        #TBD
        '''

    def deleteProject(self, cond=None, Project=None):
        '''
        #TBD
        '''


    def getFunction(self, cond=None):
        query  = "SELECT * FROM code ";

        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)
        
        query = query + conditionString

        print(query)

        ret = self.__runeMysql.sendRawQuerySelect(query, 1)

        return ret

    def getFunctionList(self, start=None, count=None, cond=None):
        query  = "SELECT * FROM code ";
        
        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)

        query = query + conditionString

        if start != None:
            query += " OFFSET = " + start

        if count is None:
            count = 0

        print(query)
        
        ret = self.__runeMysql.sendRawQuerySelect(query, count)
        return ret

    def setFunction(self, function):
        query = "INSERT INTO code(projectid, name, code, last_update) VALUES(\""+str(function.getProjectId())+"\",\""+function.getName()+"\",\""+function.getCode()+"\", CURRENT_TIMESTAMP)"

        print(query)

        ret = self.__runeMysql.sendRawQueryInsert(query)

        return ret

    def updateFunction(self, cond=None, function=None):
        query= "UPDATE code SET name=\""+function.getName()+"\" , code=\""+function.getCode()+"\" ";

        conditionString = ""
        if cond != None:
            conditionString = self.__generateCondition(cond)

        query = query + conditionString

        print(query)

        ret = self.__runeMysql.sendRawQueryUpdate(query)
        return ret

        '''
        #query = "UPDATE code SET * WHERE= "
        #TBD
        '''

    def deleteFunction(self, cond=None, function=None):
        '''
        #query = "DELETE user FROM code WHERE= "
        #TBD
        '''



