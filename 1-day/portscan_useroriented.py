# -*- coding: utf-8 -*-
from pyfiglet import *
from art import *
import cowsay


class Style:
    red = '\033[1;31m'
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    bold = "\033[1m"
    end = "\033[0m"


os.system('')


def welcome():
    # windows cmd提示符需要先输入 os.system('')才能改变终端颜色
    cowsay.pig('Thanks for using QT-PortScan')
    print(Style.yellow + "[*] Using -h/--help for more info.\n" + Style.end)


def help_info():
    print(Style.bold + "Name" + Style.end)
    print("\t juliao_demo.py - QT-PortScan help summary page")
    print(Style.bold + "SYNOPSIS" + Style.end)
    print("\t juliao_demo.py COMMAND | <flags>")
    print(Style.bold + "DESCRIPTION" + Style.end)
    print("\t QT-PortScan is a awesome port scan integration tool")
    print("\t Example:")
    print("\t\t python3 juliao_demo.py www.baidu.com 0-65535")
    print("\t\t python3 juliao_demo.py 192.168.1.1 0-65535")
    print("\t\t python3 juliao_demo.py www.baidu.com 80,443,8080,3306")
    print("\t\t python3 juliao_demo.py www.baidu.com")
    print("\t\t python3 juliao_demo.py 192.168.1.0/24 0-65535")


def banner():
    the_banner = text2art("QT-PortScan", font="tarty2")
    print(the_banner)

