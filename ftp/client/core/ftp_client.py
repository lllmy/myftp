import os
import json
import hashlib
from ftp.client.conf.conf import configuration
from ftp.client.core.file_handle import File_handle
from ftp.client.core.socket_client import MySocketClient

class FTP_client:
    def __init__(self,usr,path):
        self.usr = usr
        self.root_path = path
        self.current_path = path
        self.sk = MySocketClient()
        self.coding = configuration['coding']

    def get_dir(self):
        self.sk.sk_send({"operation": 'ls',
                         "current_path": self.current_path,
                         "username": self.usr
                         })
        data = self.sk.sk_recv()
        return data

    def show_ls(self,data):
        if data[0] and type(data[1]) is dict and data[1]['file'] or data[1]['dir'] :
            if data[1]['dir']:
                print('文件夹 ： ')
                for i in data[1]["dir"]:
                    print('\t',i)
            if data[1]['file']:
                print('文件 ： ')
                for i in data[1]["file"]:
                    print('\t',i)
        elif data[0]:
            print('当前目录为空')
        else:
            print(data[1])

    def file_send(self, file_obj,start=0):
        m = hashlib.md5()
        file_obj.processBar(start, os.path.getsize(file_obj.file_path))
        for content in file_obj.read_in_block(start):
            m.update(content)
            self.sk.sk.sendall(content)
            start += len(content)
            file_obj.processBar(start, os.path.getsize(file_obj.file_path))
        server_md5 = self.sk.sk_recv()
        if type(server_md5) is list and server_md5[0] == m.hexdigest():
            print('\033[1;32;m上传成功！\033[0m')

    def upload(self):
        filepath = input('请输入要上传的文件路径 ：').strip().rstrip(os.sep)
        if os.path.isfile(filepath):
            file_handle = File_handle(filepath)
            self.sk.sk_send({"operation": 'upload',
             "current_path": self.current_path,
             "file_name": file_handle.filename,
             "username": self.usr
             })
            result = self.sk.sk_recv()
            if result[0]:
                head = bytes(json.dumps({'operation':'send_file',
                        'file_size': file_handle.file_size
                }),encoding=self.coding)
                self.sk.struct_send(head)
                self.file_send(file_handle)
            else:
                filesize_server = result[1]
                filemd5_server = result[2]
                re = file_handle.check_file(filesize_server,filemd5_server)
                if re:
                    head = bytes(json.dumps({'operation': 'resume_breakpoint',
                                             'file_size': file_handle.file_size-filesize_server,
                                             }),encoding=self.coding)
                    self.sk.struct_send(head)
                    self.file_send(file_handle,filesize_server)

                else:
                    head = bytes(json.dumps({'operation': 'quit'}),encoding=self.coding)
                    self.sk.struct_send(head)
        else:
            print('对不起，您输入的文件路径不存在。')

    def download(self):
        pass

    def ls(self):
        data = self.get_dir()
        self.show_ls(data)

    def cd_back(self):
        path_lst = (self.current_path.rstrip(os.sep)).split(os.sep)
        path_lst.pop()
        cur_path = (os.sep).join(path_lst)
        if self.root_path in cur_path:
            self.current_path = cur_path
            print('已经返回上一层目录，本层目录下的内容如下：')
            self.ls()
        else:
            print('已经到达您的根目录，不能再返回上一层')

    def cd(self):
        data = self.get_dir()
        while True:
            self.show_ls(data)
            dir_name = input("请输入要进入的文件夹名，按q退出本次操作 : ")
            if dir_name == 'q':
                return
            elif dir_name.strip() in data[1]['dir']:
                self.current_path = os.path.join(self.current_path,dir_name)
                data = self.get_dir()
                print('已经进入新目录：%s'%dir_name)
                self.show_ls(data)
                return
            else:
                print('对不起，您输入的文件夹不存在，请更正。')

    def mk_dir(self):
        data = self.get_dir()
        dir_name = input('请输入您要创建的文件夹名,按q退出本次操作：')
        if dir_name == 'q':
            return
        elif dir_name in data[1]['dir']:
            print("对不起，您输入的文件夹已经存在。")
        elif dir_name:
            self.sk.sk_send({"operation": 'mk_dir',
                             "current_path": self.current_path,
                             "dir_name":dir_name,
                             "username": self.usr
                             })
            data = self.sk.sk_recv()
            print('\033[1;32;m文件夹创建已成功！\033[0m')
            self.show_ls(data)

    def myquit(self):
        self.sk.sk_send({'operation': 'myquit'})
        self.sk.close()
        quit()

def choose_operation(user,root_path):
    ftp_client = FTP_client(user,root_path)
    operate_dic = {'上传文件':ftp_client.upload,
                    '下载文件':ftp_client.download,
                    '查看当前目录':ftp_client.ls,
                    '返回上一级目录':ftp_client.cd_back,
                    '进入下一级目录':ftp_client.cd,
                    '创建文件夹':ftp_client.mk_dir,
                    '退出':ftp_client.myquit}
    operation_lst = ['上传文件','下载文件','查看当前目录','返回上一级目录',
                    '进入下一级目录','创建文件夹','退出']
    while True:
        for n,o in enumerate(operation_lst,1):
                print(n,o)
        try:
            num = int(input('请输入序号选择您要进行的操作：'))
            operate = operation_lst[num-1]
        except:
            print("您输入的序号有误，请重新输入。")
            continue
        func = operate_dic[operate]
        func()

if __name__ == '__main__':pass
    # path = '/Users/apple/Desktop/day7.mov'
    # path1='/Users/apple/Desktop/work/题目汇总/测试题/全栈班月考1/py4基础测试题1'
    # path2 = '/Users/apple/Desktop/work/备课/前端-this&函数调用.pptx'
    # print(os.path.isfile(path))
    # with open('/Users/apple/Desktop/day7.mov','r',encoding='utf-8') as f:
    #     while True:
    #         r = f.read(1024)
    #         print(r)
    #         if not r:
    #             break
