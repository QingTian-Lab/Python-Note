#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
主体逻辑：
1-初始化（检查参数合法性）
2-将ip和port分别加入列表
3-循环把列表内内容入参到scan函数
4-scan函数将会执行 ip数x端口数 次
4-格式化输出结果

特性：
1-无需管理员权限
2-支持CIDR类型IP
3-支持80,443 or 1000-2000 or 80 类型到端口表示方法
4-美化输出结果
5-支持ip x port 交叉合集一起扫描，也就是多ip多端口扫描

缺点：
connect方法需要建立完整tcp连接
    用threading实现多线程扫描到不到预期，出现很多不可预测行为
    扫描速度会比synscan慢
    将会在网络设备或操作系统留下痕迹
    大规模扫描可能会不准确，
Python不适合做网络端口扫描
    Python解释器运行速度太慢
    Python没有真正的多线程
优化空间
    代码过于冗余，实现不够清晰效率
    语法不够标准
    不支持外部文件输入
    不支持外部文件输出
    不支持将URL作为目标
    未模块化，外部调用可能会有麻烦

'''

import socket
import sys
import time
from ipaddress import ip_network

# 定义一个名为scan的函数,并且定义两个参数ip和port
# scan函数为程序核心功能代码
color_R = "\033[1;31m"
color_G = "\033[1;32m"
color_Y = "\033[1;33m"
color_B = "\033[1;34m"
color_end = "\033[0m"


def scan(ip, port):
    # 异常处理头
    try:
        # 初始化socket
        s = socket.socket()

        # 超时时间为2秒
        s.settimeout(0.1)

        # 发起connect方法
        #print(ip, port)
        s.connect((ip, port))

        # 关闭连接
        s.close()

        print(color_G + "[+]" + color_end + " " + str(ip) + " " + str(port) + " " + "open")
    # 异常接收
    except Exception as e:
        print(color_R + "[-]" + color_end + " " + str(ip) + " " + str(port) + " " + "close")



if __name__ == "__main__":
    version = 1.0
    arg_ip_list = []
    arg_port = []

    banner = '''
    ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║
    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
    ██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                            version: {}
                                                            
                                                            '''.format(version)
    print(banner)

    # 参数数量不是3或为-h或为--help时，输出提示语,否则把第二个参数传递给arg_ip
    if len(sys.argv) != 3 and len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(f"Usage: python3 {sys.argv[0]} <IP|IP/CIDR> <22|80,443|1000-2000>")
        exit(0)
    else:
        arg_ip = sys.argv[1]

    # 判断ip地址或者cidr是否合法
    try:
        arg_ip = ip_network(arg_ip, strict=False)
    except ValueError:
        print(color_R + "[-]" + color_end + " IP格式错误" + " " + arg_ip)
        exit(0)

    try:
        # 如果存在参数2，也就是第三个参数，如果不存在将不会执行else，会进入异常处理
        # 原因？
        # 如果写成 if sys.argv[2] == True: if下面但语句将不会被执行,也不会进入异常处理
        if sys.argv[2]:
            # 如果外部输入端口参数，就把输入值加入arg_port列表
            arg_port.append((sys.argv[2]))

    except Exception:
        arg_port = [22, 80, 443, 8080]
        print("{}[*] 将扫描默认常用端口{}".format(color_Y, arg_port))

    # 指定位置参数检查，如果给了端口参数就赋值，没给就扫默认端口
    # 由于ipaddress.ip_network函数是用来判断ip网络的，不是判断ip的，同时不想多余调用ipaddress.ip_address，所以参数是ip地址的时候\
    # 用户传入的arg_ip还是会带有/24等cidr形式，所以要做字符串处理

    # 如果ip地址里没有/，就把ip地址传递给arg_ip，否则就把所有目标ip列出来并且添加进arg_ip_list列表
    if "/" not in sys.argv[1]:
        # 就算是一个ip也添加进列表，统一格式方便调用
        arg_ip_list.append(sys.argv[1])
        arg_ip = str(arg_ip_list)
    else:
        # ip格式校验
        try:
            for arg_ip in ip_network(sys.argv[1], strict=False):
                # 把目标循环添加到ip_list列表并且转换为str类型
                arg_ip_list.append(str(arg_ip))

            # 此时到arg_ip已经是一个列表合集
            arg_ip = str(arg_ip_list)

        # 如果ip值异常异常就报错
        except ValueError as error:
            print(color_R + " " + arg_ip)
            exit(0)

    # 判断端口输入是否合法
    try:
        # 检查列表元素里的端口是否合法,该if如果抛出异常说明列表内的数据类型不是int，所以无法比较
        if all((1 <= int(_) <= 65535 for _ in arg_port)):
            pass
        else:
            print(color_R + "[-]" + color_end + " 输入端口超出范围" + " " + str(arg_port))
            exit(0)
    except Exception:
        # 上面if如果抛出异常说明列表内的数据类型不是int，所以无法比较，将打印 端口输入异常
        print(color_R + "[-]" + color_end + " 端口输入异常" + " " + str(arg_port))
        exit(0)

    # 这里格式化不够清晰，代码阅读性太差
    print("{}[*] {} 开始扫描{}个IP，{}个端口".format(color_Y, time.strftime('%H:%M:%S'), len(arg_ip_list), len(arg_port)))


    # 开始扫描
    try:
        for i in arg_ip_list:
            for p in arg_port:
                scan(str(i), int(p))
    except KeyboardInterrupt as error:
        print('\n{}[*] {} 手动结束了扫描'.format(color_Y,time.strftime('%H:%M:%S')))
    #print('共用时{}'.format(time.thread_time()))

