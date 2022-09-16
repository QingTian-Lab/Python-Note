#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import portscan_scanoriented as ps
from socket import *


def scan_thread(scan_target, scan_ports):
    thread_list = []
    for port in scan_ports:
        thread_object = threading.Thread(target=ps.port_scan(),
                                         args=(gethostbyname(),
                                               int(port)))
        thread_object.setDaemon(True)
        thread_list.append(thread_object)

    del thread_object
    for thread_object in thread_list:
        thread_object.start()

    del thread_object
    for thread_object in thread_list:
        thread_object.join()

    for open_port in port:
        print(f"Target:{scan_target} -- IP: {gethostbyname(scan_target)} -- Port:{open_port} ---> open!")
    del thread_object
    print("Scan Finished!")