# -*- coding: utf-8 -*-
"""
-*- coding: utf-8 -*-
@Author: XF010101
@SoftWare: PyCharm
@File: ssaskclient.py
@Time: 2022/6/13 12:16
"""
import socket
import threading


def encodeL(text):
    # 加密
    text2 = ''  # 用来存放加密之后的内容
    i = 0
    # 用循环是为了替换掉文本中的每一个字符
    while i < len(text):
        # ord(text[i]) 意为先将字符转为ASCII码
        # chr(...) 意为将处理好的ASCII码转换成字符
        text2 = text2 + chr(ord(text[i]) + 1)
        i = i + 1
    return text2


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


def recv(sock, addr):
    '''
    一个UDP连接在接收消息前必须要让系统知道所占端口
    也就是需要send一次，否则win下会报错
    '''
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        datadecode = data.decode('utf-8')
        if " : " in datadecode:
            datastr = datadecode.split(' : ')[0] + " : " + decodeL(datadecode.split(' : ')[1])
        else:
            datastr = datadecode
        print(datastr)


def send(sock, addr):
    '''
        发送数据的方法
        参数：
            sock：定义一个实例化socket对象
            server：传递的服务器IP和端口
    '''
    while True:
        string = input('')
        message = name + ' : ' + encodeL(string)
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.lower() == 'EXIT'.lower():
            break


def main():
    '''
        主函数执行方法，通过多线程来实现多个客户端之间的通信
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ('x.x.x.x', 7878)
    tr = threading.Thread(target=recv, args=(s, server), daemon=True)
    ts = threading.Thread(target=send, args=(s, server))
    tr.start()
    ts.start()
    ts.join()
    s.close()


if __name__ == '__main__':
    print("-----欢迎来到聊天室,退出聊天室请输入'EXIT(不分大小写)'-----")
    name = input('请输入你的名称:')
    print('-----------------%s------------------' % name)
    main()
