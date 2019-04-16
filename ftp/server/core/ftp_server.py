import os
import json
import struct
import hashlib
from ftp.server.core import file_handle

def ls(user_info,usr,current_path):
    if user_info.user_dic[usr]["root_path"] in current_path:
        try:
            dir_list = os.listdir(current_path)
            ls_dic = {'dir':[],'file':[]}
            for i in dir_list:
                filepath = os.path.join(current_path, i)
                if os.path.isdir(filepath):
                        ls_dic['dir'].append(i)
                elif os.path.isfile(filepath):
                        ls_dic['file'].append(i)
        except Exception as e:
            return [False, "错误的目录"]
        return [True, ls_dic]
    else:
        return [False, "错误的目录"]

def mk_dir(user_info,usr,current_path,dir_name):
    if user_info.user_dic[usr]["root_path"] in current_path:
        new_path = os.path.join(current_path,dir_name)
        os.mkdir(new_path)
    return ls(user_info,usr,current_path)

def recv_file(file_path,file_size_client,sk,mode):
    m = hashlib.md5()
    with open(file_path, mode) as f:
        while file_size_client:
            if file_size_client > 1024:
                content = sk.conn.recv(1024)
                file_size_client -= 1024
            else:
                content = sk.conn.recv(file_size_client)
                file_size_client -= file_size_client
            if content == b'':
                break
            f.write(content)
            m.update(content)
    return m.hexdigest()

def upload(user_info,usr,current_path,file_name,sk):
    if user_info.user_dic[usr]["root_path"] in current_path:
        file_path = os.path.join(current_path,file_name)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            file_md5 = file_handle.check_md5(file_path)
            sk.my_send([False,file_size,file_md5])
        else:
            sk.my_send([True])
        result = sk.conn.recv(4)
        read_size = struct.unpack('i', result)[0]
        result = sk.conn.recv(read_size).decode('utf-8')
        result = json.loads(result)
        if result['operation'] == 'quit':
            return
        elif result['operation'] == 'resume_breakpoint':
            file_size_client = result['file_size']
            file_md5 = recv_file(file_path,file_size_client,sk,'ab')
            sk.my_send([file_md5])
            return
        elif result['operation'] == 'send_file':
            file_size_client = result['file_size']
            file_md5 = recv_file(file_path, file_size_client, sk,'wb')
            sk.my_send([file_md5])
            return


