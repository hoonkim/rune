#!/usr/bin/python3

import pymysql

#conn = pymysql.connect(host = "175.126.112.130", user="rune", password="fjsld89", db="rune_dev", charset="utf8mb4")


RuneConn = RuneMySQLConnector(serverHost="175.126.112.130", userId="rune", userPw="fjsld89", userDb="rune_dev")
RuneConn.sendRawQueryInsert("INSERT INTO test VALUES(0, 'HELLO_WORLD')";

class  RuneMySQLConnector:
    __conn = None

    __host = None
    __port = None
    __userId = None
    __userPw = None
    __userDb = None

    def __init__(self, serverHost=None, serverPort=None, userId=None, userPw=None, userDb = None, userCharset = None):
        if host != None:
            self.__host = host
        else:
            self.__host = "127.0.0.1"

        if port != None:
            self.__port = None
        else:
            self.__port = "3306"

        if userId != None:
            self.__userId = userId            

        if userPw != None:
            self.__userPw = userPw

        if userDb != None:
            self.__userDb = userDb

        if userCharset != None:
            userCharset = "utf8mb4"


        try:
            self.__conn = pymysql.connect(host=self.__host, user=self.__userId, password=self.__userPw, db=self.__userDb, charset=userCharset)
        except ProgrammingError as e:
            print ("mysql connect exception")
            print (e)


    def sendRawQuerySelect(self, queryString, count=0):
        try:
            with self.__conn.cursor() as cursor:
                sql =queryString
                cursor.execute(sql)
                if count == 0:
                    self.__conn.fetchall()
                else:
                    self.__conn.fetchmany(count)
        finally:
            self.__conn.close()

    def sendRawQueryInsert(self, queryString):
        try:
            with self.__conn.cursor() as cursor:
                sql =queryString
                cursor.execute(sql)
                cursor.commit()

                sql = "SELECT last_insert_id()"
                cursor.execute(sql)
                ret = cursor.fetchone()[0]
        finally:
            self.__conn.close()

        return ret

    def sendRawQueryUpdate(self, queryString):
        try:
            with self.__conn.cursor() as cursor:
                sql =queryString
                cursor.execute(sql)
                cursor.commit()

        finally:
            self.__conn.close()