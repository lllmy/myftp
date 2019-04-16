import os
import hashlib

def read_in_block(file_path):
    BLOCK_SIZE = 1024
    m = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            block = f.read(BLOCK_SIZE)  # 每次读取固定长度到内存缓冲区
            if block:
                m.update(block)
                yield block
            else:
                return m.hexdigest()   # 如果读取到文件末尾，则退出

def check_md5(file_path,check_size=None, start_position=0):
    m = hashlib.md5()
    check_size = check_size if check_size else os.path.getsize(file_path)
    block = int(check_size / 10) if check_size > 1024 * 10 else 1024
    with open(file_path, "rb") as f:
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

