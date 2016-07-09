from handler import *

PORT = 8000

server = ThreadedHTTPServer(('localhost', PORT), SentinelHttpHandler)
print('Starting server, use <Ctrl-C> to stop')
server.serve_forever()