import sys
sys.path.insert(0, '../runeHTTP')

from time import sleep

from requestList import RuneRequestList
from request import RuneRequest, RuneRequestSender

class SentinelRequestList(RuneRequestList):
    def __init__(self):
        '''
        '''