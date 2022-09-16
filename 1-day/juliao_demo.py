#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import sys
import threading
import portscan_useroriented as pu
import portscan_scanoriented as ps
import portscan_threadoriented as pt
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

#host = sys.argv[1]
"""
@ split
  1.语法：str.split(str="", num=string.count(str))
    - str: 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
    - num: 分割次数。默认为 -1, 即分隔所有
  2. 返回值为分割后的字符串列表
  2.如用户输入 1000-3000，经处理后为：['1000', '3000']
"""
# port_range = sys.argv[2].split('-')
#
# # 定义起始端口和结束端口，接收来自 split 处理的结果
# start_port = int(port_range[0])
# end_port = int(port_range[1])
# # 调用 socket 下的 gethostbyname 来解析目标 IP
# target_ip = gethostbyname(host)
# # 创建列表 opened_port 保存目标开放的端口
# opened_ports = []


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print(f"Usage:{sys.argv[0]} [host] [start_port]-[end_port]")
    #     pu.tips()
    #     exit(0)
    # pu.banner()
    if len(sys.argv) == 1:
        pu.welcome()
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        pu.help_info()
    elif ps.is_ip(sys.argv[1]) and ps.is_port(sys.argv[2]):
        print("Start Scan")
    else:
        print("something")











