#import sys
from message_listener import *

if __name__ == "__main__":
    listener = MessageListener("localhost", "wisp")

    print("Wisp now working press ctrl + c to stop")
    listener.listen()

