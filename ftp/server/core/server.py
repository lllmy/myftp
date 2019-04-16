from ftp.server.core import user as user_lib
from ftp.server.core import ftp_server

class Views:

    user_info = user_lib.UserInfo()

    @staticmethod
    def login(info):
        login_result = Views.user_info.auth(info['username'],info['password'])
        return login_result

    @staticmethod
    def register(info):
        regist_result = Views.user_info.register(info['username'],info['password'])
        return regist_result

    @staticmethod
    def ls(info):
        ls_result = ftp_server.ls(Views.user_info,info['username'],info["current_path"])
        return ls_result

    @staticmethod
    def mk_dir(info):
        mkdir_result = ftp_server.mk_dir(Views.user_info,info['username'],
                                         info['current_path'],
                                         info['dir_name'])
        return mkdir_result

    @staticmethod
    def upload(info):
        username = info['username']
        current_path = info['current_path']
        file_name = info["file_name"]
        sk = info['socket']
        ftp_server.upload(Views.user_info,username,current_path,file_name,sk)