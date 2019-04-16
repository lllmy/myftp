import os
import sys
import hashlib
from ftp.server.conf.conf import configuration
class UserInfo:
    __instance = None
    #server_path_lst = sys.path[0].split('/')[:-1]
    server_path_lst = sys.path[0].split(os.sep)[:-1]
    server_path_lst.extend(['db','user_info'])
    server_path = (os.sep).join(server_path_lst)
    ftp_root = configuration['ftp_root']
    auth_key = configuration['auth_key']
    coding = configuration['coding']

    def __new__(cls, *args, **kwd):
        if UserInfo.__instance is None:
            UserInfo.__instance = object.__new__(cls, *args, **kwd)
            cls.load_user_info()
        return UserInfo.__instance

    @classmethod
    def get_pwd(cls,pwd):
        hash = hashlib.md5(pwd.encode(encoding=cls.coding))
        hash.update(cls.auth_key.encode(encoding=cls.coding))
        return hash.hexdigest()

    @classmethod
    def load_user_info(cls):
        cls.user_dic = {}
        with open(UserInfo.server_path,'r') as f:
            for info in f:
                username,password = info.split()
                root_path = '%s%s%s' % (UserInfo.ftp_root, os.sep, username)
                cls.user_dic[username] = {'password':password,'times':0,'root_path':root_path}
                if not os.path.exists(root_path):
                    os.mkdir(root_path)

    @classmethod
    def auth(cls,usr,pwd):
        pwd = cls.get_pwd(pwd)
        if cls.user_dic.get(usr) and cls.user_dic[usr]['times']<3 and cls.user_dic[usr]['password'] == pwd:
            cls.user_dic[usr]['times'] += 0
            return [True,'Login success.',cls.user_dic[usr]['root_path']]
        elif cls.user_dic.get(usr) and cls.user_dic[usr]['times']<3:
            cls.user_dic[usr]['times'] += 1
            return [False,'Sorry,you had a bad pwd.']
        elif cls.user_dic.get(usr) and cls.user_dic[usr]['times']==3:
            return [False,'Your account has been disabled.']
        else:
            return [False,'The username is not exit.']

    @classmethod
    def register(cls,usr,pwd):
        if usr in cls.user_dic.keys():
            return [False, '您注册的用户名已存在，请更换。']
        else:
            pwd = cls.get_pwd(pwd)
            cls.user_dic[usr] = {'password': pwd, 'times': 0}
            with open(UserInfo.server_path, 'a') as f:
                f.write('\n%s %s'%(usr,pwd))
            root_path = '%s%s%s'%(UserInfo.ftp_root,os.sep,usr)
            os.mkdir(root_path)
            cls.user_dic[usr]['root_path'] = root_path
            return [True, '注册成功！',cls.user_dic[usr]['root_path']]

if __name__ == '__main__':
    print(os.pathsep)
    print(os.sep)
    # userinfo = UserInfo()
    # print(id(userinfo))
    # print(userinfo.user_dic)
    # userinfo.user_dic['eva']['times']+=1
    # print(userinfo.user_dic)
    # userinfo = UserInfo()
    # print(id(userinfo))
    # print(userinfo.user_dic)