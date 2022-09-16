# -*- coding: utf-8 -*-
import os
import socket
import sys
import time
from ipaddress import *
from socket import *


class Style:
    red = '\033[1;31m'
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    bold = "\033[1m"
    end = "\033[0m"


os.system('')


def is_ip(scan_target_ip):
    target_ip = ip_network(scan_target_ip, strict=False)
    try:
        target_ip = ip_network(scan_target_ip, strict=False)
        return True
    except ValueError:
        print(Style.Style.red + "[-]" + Style.end + target_ip + " " + "Not a IP")
        return False


def is_port(scan_port):
    # 端口合法性检查：
    try:
        # 检查列表元素里的端口是否合法,该if如果抛出异常说明列表内的数据类型不是int，所以无法比较
        # if all((1 <= int(_) <= 65535 for _ in scan_port)):
        #     return True
        if 1 <= int(scan_port) <= 65535:
            return True
        else:
            print(Style.red + "[-]" + Style.end
                  + " Port range out of scope."
                  + " " + str(scan_port))
            return False
    except Exception:
        # 上面if如果抛出异常说明列表内的数据类型不是int，所以无法比较，将打印端口输入异常
        print(Style.red + "[-]" + Style.end
              + " Exist illegal port! Please Check the variable type"
              + " " + str(scan_port))
        return False


def print_success(msg):
    print(f"{Style.green}[+]{Style.end} {msg}")


def port_scan(scan_target, scan_port):
    opened_ports = []
    scan_target_ip = gethostbyname(scan_target)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((scan_target_ip, scan_port))
        if result == 0:
            opened_ports.append(scan_port)
        sock.close()
    except KeyboardInterrupt:
        print("You Pressed Ctrl+C")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved, try -h/--help for more info. Exiting")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()
    except Exception as e:
        print(e)


def port_list(scan_target, scan_ports):
    ports = []
    try:
        if scan_ports:
            ports.append(scan_ports)
        else:
            print("Will Scan the Default Ports: 1-1000.")
            # 跳转到扫描端口范围函数
    except Exception as e:
        print("error")

    for p in ports:
        port_scan(scan_target, p)


def port_range(scan_target, scan_port_range):
    start_port = int(scan_port_range[0])
    end_port = int(scan_port_range[1])

    for p in range(start_port, end_port):
        port_scan(scan_target, p)


def cidr(scan_target, scan_ports):
    scan_target_ip = []
    try:
        for ip in ip_network(scan_target, strict=False):
            scan_target_ip.append(ip)
    except ValueError as e:
        print(Style.red + " " + ip)
        exit(0)

    for i in scan_target_ip:
        port_scan(i, scan_ports)


# def port_file():
