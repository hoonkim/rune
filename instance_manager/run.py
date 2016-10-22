from http.server import HTTPServer

import server

PORT = 8000

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('127.0.0.1', 8080), server.InstanceManagerServer)
    print("ctrl + c  to exit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()