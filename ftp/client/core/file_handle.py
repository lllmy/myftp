import os
import sys
import hashlib
from ftp.client.conf.conf import configuration
class File_handle:
    def __init__(self,file_path):
        self.file_path = file_path
        self.filename = file_path.split(os.sep).pop()
        self.file_size = os.path.getsize(file_path)
        self.block_size = configuration['block_size']

    def read_in_block(self,start=0):
        read_size = self.file_size - start
        with open(self.file_path, "rb") as f:
            f.seek(start)
            while True:
                if  read_size > self.block_size:
                    block = f.read(self.block_size)  # 每次读取固定长度到内存缓冲区
                    read_size -= self.block_size
                else:
                    block = f.read(read_size)
                    read_size -= read_size
                if block:
                    yield block
                else:
                    return

    def check_md5(self, check_size=None,start_position=0):
        m = hashlib.md5()
        block = int(check_size / 10) if check_size > 1024 * 10 else 1024
        with open(self.file_path, "rb") as f:
            f.seek(start_position)
            while check_size:
                if check_size > block:
                    content = f.read(1024)
                    m.update(content)
                    f.seek(f.tell() - 1024 + block)
                    check_size -= block
                else:
                    f.read(check_size)
                    m.update(content)
                    check_size -= check_size
        return m.hexdigest()

    def check_file(self,filesize_server,filemd5_server):
        file_md5 = self.check_md5(filesize_server)
        if os.path.getsize(self.file_path) > filesize_server and file_md5 == filemd5_server:
                go_on = input('文件已上传了一部分，是否需要继续(y/n)：')
                if go_on == 'y':
                    return True
        else:
            print('对不起，已经有一个同名文件存在。')

    @staticmethod
    def processBar(num, total):
        rate = num / total
        rate_num = int(rate * 100)
        if rate_num == 100:
            r = '\r%s>%d%%\n' % ('=' * rate_num, rate_num,)
        else:
            r = '\r%s>%d%%' % ('=' * rate_num, rate_num,)
        # sys.stdout.write(r)
        # sys.stdout.flush
        print(r,end='', file=sys.stdout, flush=True)



