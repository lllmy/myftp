import hashlib
def check_md5(file_path,check_size=None, start_position=0):
    m = hashlib.md5()
    block =int(check_size / 10) if check_size > 1024*10 else 1024
    with open(file_path, "rb") as f:
        f.seek(start_position)
        while check_size:
            if check_size > block:
                content = f.read(1024)
                m.update(content)
                f.seek(f.tell()-1024+block)
                check_size -= block
            else:
                f.read(check_size)
                m.update(content)
                check_size -= check_size
    return m.hexdigest()

def cut_file(check_size):
    with open('/Users/apple/Desktop/day7.mov','rb') as f1,open('/Users/apple/Desktop/day7(2).mov','wb') as f2:
        while check_size:
            if check_size > 1024:
                content = f1.read(1024)
                f2.write(content)
                check_size -= 1024
            else:
                content = f1.read(check_size)
                f2.write(content)
                check_size -= check_size

# import os
# # print(os.path.getsize('/Users/apple/Desktop/day7.mov'))
#
# import time
# start = time.time()
# cut_file(7087583428)
# print(time.time()-start)
# start = time.time()
# a = check_md5('/Users/apple/Desktop/day7.mov',7087583428)
# print(time.time()-start)
# b = check_md5('/Users/apple/Desktop/day7(2).mov',os.path.getsize('/Users/apple/Desktop/day7(2).mov'))
# print(a)
# print(b)