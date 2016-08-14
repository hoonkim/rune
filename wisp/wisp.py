import wisp.message_listener
#import sys

if __name__ == "__main__":
    listener = wisp.message_listener("localhost", "wisp")

    print("Wisp now working press ctrl + c to stop")
    listener.listen()

