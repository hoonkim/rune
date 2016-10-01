import sys
sys.path.insert(0, '../runeconnect')

from time import sleep

from requestlist import RuneRequestList
from request import RuneRequest, RuneRequestSender

class SentinelRequestList(RuneRequestList):
    def __init__(self):
        '''
        '''
