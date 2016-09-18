#Client instance information
from enum import Enum


class InstanteStatus(Enum):
    INSTANCE_OFF = 0
    INSTANCE_READY = 1
    INSTANCE_RUNNING = 2


class Instance:
    _id = None
    _address = None
    _state = None

    def __init__(self, serverId, serverAddress):
        self._serverId = serverId
        self._serverAddress = serverAddress

    def getInstnaceStatus(self):
        



