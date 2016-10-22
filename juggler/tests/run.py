
from handler import *

PORT = 8000

server = ThreadedHTTPServer(('127.0.0.1', PORT), RuneHttpHandler)
print('Starting server, use <Ctrl-C> to stop')
server.serve_forever()
