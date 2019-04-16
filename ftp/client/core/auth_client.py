import json
from ftp.client.conf import conf
from ftp.client.core.socket_client import MySocketClient
class myclient:
    def __init__(self):
        self.sk = MySocketClient()
        self.name = None

    def login(self):
        flag = True
        while flag:
            usrname = input('请输入您的用户名,按q退出登陆 : ')
            if usrname == 'q':
                return {'operation': 'login', 'result': False}
            passwd = input('请输入密码 : ')
            if usrname and passwd:
                info = {'operation':'login','username':usrname,'password':passwd}
                self.sk.sk_send(info)
                ret = self.sk.sk_recv()
                print('\033[1;32;m%s\033[0m'%ret[1])
                if ret[0]:
                    self.name = usrname
                    return {'operation':'login',
                            'result':True,
                            'root_path':ret[2]}

    def register(self):
        while True:
            usrname = input('请输入您要注册的用户名，按q退出注册 ：')
            if usrname == 'q':
                return {'operation': 'register', 'result': False}
            elif usrname:
                while True:
                    passwd = input('请设置登陆密码 ：')
                    passwd_confirm = input('请再次输入密码 ：')
                    if passwd == passwd_confirm:
                        sk = MySocketClient()
                        info = {'operation': 'register', 'username': usrname, 'password': passwd}
                        sk.sk_send(info)
                        ret = sk.sk_recv()
                        print('\033[1;32;m%s\033[0m'%ret[1])
                        if ret[0]:
                            self.name = usrname
                            return {'operation': 'register',
                                    'result': True,
                                    'root_path':ret[2]}
                        break
                    else:
                        print('两次输入的密码不一致，请重新输入。')

    def myquit(self):
        self.sk.sk_send({'operation': 'myquit'})
        self.sk.close()
        exit()

if __name__ == '__main__':
    pass
