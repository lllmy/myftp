import json
import socketserver
from ftp.server.core.server import Views
class MyServer(socketserver.BaseRequestHandler):
    def my_send(self,content):
        content = json.dumps(content)
        send_content = bytes(content, encoding='utf-8')
        try:
            self.conn.sendall(send_content)
        except:
            print('客户端由于网络原因断开链接。')
            return False

    def my_recv(self):
        try:
            jdata = self.conn.recv(1024).decode('utf-8')
            data = json.loads(jdata)
            return data
        except Exception as e:
            print(e)
            #print('客户端由于网络原因断开链接。')
            return False

    def handle(self):
        self.conn = self.request
        Flag = True
        while Flag:
            data = self.my_recv()
            if type(data) is dict and data['operation'] == 'myquit':
                Flag = False
            elif type(data) is dict and hasattr(Views,data['operation']):
                func = getattr(Views,data['operation'])
                data['socket'] = self
                result = func(data)
                if result:
                    self.my_send(result)
            else:
                break

if __name__ == '__main__':
    import socketserver
    from ftp.server.conf.conf import *
    server = socketserver.ThreadingTCPServer((configuration.get('server_ip'),configuration.get('server_port')),MyServer)
    server.allow_reuse_address = True
    server.serve_forever()