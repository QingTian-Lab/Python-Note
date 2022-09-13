import socket
import threading
import sys
import re

L = threading.BoundedSemaphore(1000)
def Scan_Thread(Target,Port):
    L.acquire()
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((Target,Port))
        sock.close()
        print(f"IP:{Target} Port:{Port} --- open ")
    except Exception as error:
        pass
    L.release()
def ip(s):
    p = '((\d{1,2})|([01]\d{2})|(2[0-4]\d)|(25[0-5]))'
    pattern = '^' + '\.'.join([p]*4) +'$'
    return bool(re.match(pattern,s))
def main():
    str = 'portscan_crow Version 1.0'
    s = sys.argv[1]
    print(str.center(60, '*'))
    if len(sys.argv) == 2:
        if ip(s):
            Threadlist = []
            for i in range(8889):
                Threadob = threading.Thread(target=Scan_Thread,args=(sys.argv[1],i),daemon=True)
                Threadlist.append(Threadob)
                Threadob.start()
            for value in Threadlist:
                value.join()
            print("扫描结束")
        else:
            print("请检查您输入的IP地址是否正确!")
            exit(0)
    else:
        print("使用方式：",sys.argv[0],'目标IP')
        exit(0)


# C段 主机扫描
# 批量主机发现
def get_ip_list(ip):
    temp = str(ip).split('.')    # 这里定义一个临时文件temp,将输入的ip转换为字符串，并且通过split()方法进行分割，即通过指定的分割符进行分割
    ip_list = []   # 定义一个接收IP段的空列表
    for i in range(255):  # 因为IP的前三位是固定的，只需要对最后一位进行从1-254的遍历，所以使用一个for循环遍历最后一位
        ip_list.append(temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+str(i))  # 将输出的结果加入ip_list列表
    return ip_list   # 通过return 返回这个IP列表


if __name__ == '__main__':
    main()
    list = get_ip_list('192.168.1.1')
    print(list)





