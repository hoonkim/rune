#!/usr/bin/python3
import sys
sys.path.insert(0, '../runebook')
from runebook import *

#RuneConn = RuneMySQLConnector(serverHost="175.126.112.130", userId="rune", userPw="fjsld89", userDb="rune_dev")
conn = RuneBookConnect(serverHost="175.126.112.130", userId="rune", userPw="fjsld89", userDb="rune_dev")



testUser = RuneUser("foo@bar","0000")
conn.setUser(testUser)

ret = conn.getUserList()
print(ret)