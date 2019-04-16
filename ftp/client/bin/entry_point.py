from ftp.client.core import ftp_client
from ftp.client.core.auth_client import myclient
def main():
    while True:
        client = myclient()
        entry_operate = {'登陆': client.login, '注册': client.register, '退出': client.myquit}
        entry_oprt_k = ['登陆', '注册', '退出']
        for num, operate in enumerate(entry_oprt_k, 1):
            print(num, operate)
        oper = input('请输入您要进行的操作序号 ：')
        try:
            func = entry_operate[entry_oprt_k[(int(oper)) - 1]]
        except:
            print('您输入的内容有误，请再次输入。')
            continue
        ret = func()
        if client.name and ret['result'] == True:
            ftp_client.choose_operation(client.name,ret['root_path'])


if __name__ == "__main__":
    main()