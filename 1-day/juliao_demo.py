#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import threading
"""
@ import 和 form xx import * 的区别
  主要是针对socket模块 
  1. 使用 import socket 时，要用 socket.AF_INET 会报错，提示没有 AF_INET 这个族，
     是因为 AF-INET 这个值在 socket 的名称空间下
  2. from 语句不创建一个到模块名字空间的引用对象，而是把被导入模块的一个或多个对象直接放入当前的名字空间
     from socket import gethostbyname 就是把 gethostbyname 导入当前文件的命名空间
     from socket import * 是把 socket 下的所有名字引入当前的名称空间
"""

from socket import *
# 接收用户输入的参数，第一个为扫描的目标，可以为任意的host，不一定要为ip，更加弹性灵活；第二个为端口范围

host = sys.argv[1]
"""
@ split
  1.语法：str.split(str="", num=string.count(str))
    - str: 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
    - num: 分割次数。默认为 -1, 即分隔所有
  2. 返回值为分割后的字符串列表
  2.如用户输入 1000-3000，经处理后为：['1000', '3000']
"""
port_range = sys.argv[2].split('-')

# 定义起始端口和结束端口，接收来自 split 处理的结果
start_port = int(port_range[0])
end_port = int(port_range[1])
# 调用 socket 下的 gethostbyname 来解析目标 IP
target_ip = gethostbyname(host)
# 创建列表 opened_port 保存目标开放的端口
opened_ports = []


def port_scanner(scan_target_ip, scan_port):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((scan_target_ip, scan_port))
        if result == 0:
            opened_ports.append(scan_port)
        sock.close()
    except Exception as e:
        print(e)


def thread_handler():
    thread_list = []
    for port in range(start_port, end_port):
        thread_object = threading.Thread(target=port_scanner,
                                         args=(gethostbyname(sys.argv[1]),
                                               int(port)))
        thread_object.setDaemon(True)
        thread_list.append(thread_object)

    for thread_object in thread_list:
        thread_object.start()

    for thread_object in thread_list:
        thread_object.join()

    for open_port in opened_ports:
        print(f"Target:{sys.argv[1]} -- IP: {gethostbyname(sys.argv[1])} -- Port:{open_port} ---> open!")
    del thread_object
    print("Scan Finished!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage:{sys.argv[0]} [host] [start_port]-[end_port]")
        print("Example:juliao_demo.py www.baidu.com 0-65535")
        # 退出整个程序
        exit(0)
    print(
        """
          █████  ▄▄▄█████▓ ██▓███   ▒█████   ██▀███  ▄▄▄█████▓  ██████  ▄████▄   ▄▄▄       ███▄    █ 
        ▒██▓  ██▒▓  ██▒ ▓▒▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █ 
        ▒██▒  ██░▒ ▓██░ ▒░▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒
        ░██  █▀ ░░ ▓██▓ ░ ▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░   ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒
        ░▒███▒█▄   ▒██▒ ░ ▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░ ▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░
        ░░ ▒▒░ ▒   ▒ ░░   ▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
         ░ ▒░  ░     ░    ░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░    ░    ░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░
           ░   ░   ░      ░░       ░ ░ ░ ▒    ░░   ░   ░      ░  ░  ░  ░          ░   ▒      ░   ░ ░ 
            ░                          ░ ░     ░                    ░  ░ ░            ░  ░         ░ 
                                                                       ░            
                                                                            QT-PortScan version 0.0.1                                                                             
                                                                            @ QingTian Lab by Juliao
        """
    )
    thread_handler()


