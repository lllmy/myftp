import json
import struct
import socket

from ftp.client.conf.conf import *

class MySocketClient:
    __instance = None

    def __new__(cls, *args, **kwd):
        if MySocketClient.__instance is None:
            MySocketClient.__instance = object.__new__(cls, *args, **kwd)
            ip_port = (configuration.get('server_ip'), configuration.get('server_port'))
            cls.sk = socket.socket()
            cls.conn = cls.sk.connect(ip_port)
        return MySocketClient.__instance

    @classmethod
    def sk_send(cls,content):
        content = json.dumps(content)
        send_content = bytes(content, encoding='utf-8')
        cls.sk.sendall(send_content)

    @classmethod
    def sk_recv(cls):
        data = cls.sk.recv(1024).decode('utf-8')
        return json.loads(data)

    @classmethod
    def struct_send(cls,head):
        head_len = struct.pack('i', len(head))
        cls.sk.sendall(head_len)
        cls.sk.sendall(head)

    @classmethod
    def close(cls):
        cls.sk.close()

if __name__ == "__main__":
    pass
