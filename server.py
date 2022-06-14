"""
-*- coding: utf-8 -*-
@Author: XF010101
@SoftWare: PyCharm
@File: ssaskserver.py
@Time: 2022/6/13 12:15
"""
import socket
import logging

def decodeL(text2):
    text3 = ''  # 用来存放解密之后的内容
    i = 0
    # 用循环是为了替换掉文本中的每一个字符
    while i < len(text2):
        # ord(text2[i]) 意为先将字符转为ASCII码
        # chr(...) 意为将处理好的ASCII码转换成字符
        text3 = text3 + chr(ord(text2[i]) - 1)
        i = i + 1
    return text3

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象  属性为UDP连接

    addr = ('', 7878)
    s.bind(addr)  # 绑定地址和端口

    logging.info('UDP Server on %s:%s...', addr[0], addr[1])

    user = {}  # 存放字典{addr:name}
    while True:
        try:
            data, addr = s.recvfrom(1024)  # 等待接收客户端消息存放在2个变量data和addr里
            if not addr in user:  # 如果addr不在user字典里则执行以下代码
                for address in user:  # 从user遍历数据出来address
                    s.sendto(data + ' 进入聊天室...'.encode('utf-8'), address)  # 发送user字典的data和address到客户端
                user[addr] = data.decode('utf-8')  # 接收的消息解码成utf-8并存在字典user里,键名定义为addr
                continue  # 如果addr在user字典里，跳过本次循环

            if 'EXIT'.lower() in data.decode('utf-8'):  # 如果EXIT在发送的data里
                name = user[addr]  # user字典addr键对应的值赋值给变量name
                user.pop(addr)  # 删除user里的addr
                for address in user:  # 从user取出address
                    s.sendto((name + ' 离开了聊天室...').encode(), address)  # 发送name和address到客户端
            else:
                datadecode = data.decode('utf-8')
                datastr = datadecode.split(' : ')[0]+" : "+decodeL(datadecode.split(' : ')[1])
                print('"%s" from %s:%s' % (datastr, addr[0], addr[1]))
                for address in user:  # 从user遍历出address
                    if address != addr:  # address不等于addr时间执行下面的代码
                        s.sendto(data, address)  # 发送data和address到客户端

        except ConnectionResetError:
            logging.warning('Someone left unexcept.')


if __name__ == '__main__':
    main()
