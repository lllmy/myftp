import socketserver

from ftp.server.conf.conf import *
from ftp.server.core import socket_server

def main():
    server = socketserver.ThreadingTCPServer(
        (configuration.get('server_ip'),
         configuration.get('server_port')),
         socket_server.MyServer)
    server.serve_forever()

if __name__ == "__main__":
    main()