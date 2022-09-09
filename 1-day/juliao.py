#!/usr/bin/python3
# coding=utf-8

"""
@ Juliao
@ Read the Code and add Notation.
"""
import sys
import socket
import threading

# 定义布尔型变量 showerror, 初始值为 False
showerror = False

"""
@ 定义变量 pool_sema 意为信号池
    threading.BoundedSemaphore 的原型是类 class threading.BoundedSemaphore([value])
    @values：values 是一个内部计数变量，默认值为 1，如果小于 0，则会抛出 ValueError 异常
             values 用于控制线程数、并发数等
    @Semaphore：信号量
    @BoundedSemaphore：边界信号量，继承自 Semaphore 类；用作边界绑定，是有界的信号量，
                       不允许使用 release 超过初始值的范围，用于控制没有获取信号量就开始释放，
                       导致内置计数器 value 的值超出最大上限值的情况
    @acquire：信号获取，获取信号量，计数器减 1
    @release：信号释放，释放信号量，计数器加 1
"""

# 此处限制信号池数量上限为 1000, 防止程序卡死
max_connections = 1000
pool_sema = threading.BoundedSemaphore(max_connections)

# 定义函数 ScannerTread，该函数定义扫描端口时的通信过程，主要包括socket通信连接及其异常处理，
# 这种端口扫描的原理是通过与目标 IP 的特定端口建立 TCP 三次握手，如果连接成功表明 TCP 三次握手完成，此端口开放
# 需要传递两个参数，分别为 TargetIP(目标IP) 和 Port(端口号)


def ScannerThread(TargetIp, Port):
    # 变量 pool_sema 调用 thread 库中的 acquire 方法，获取信号量
    pool_sema.acquire()
    """
    @ 使用try ... except ...结构，用于抛出异常并继续执行代码
      1.代码结构
        try: 
            ... 
        except error1,error2,... as e:
            ...
        except error3,error4,... as e:
            ...
        except Exception:
            ...
      2.执行顺序
        - 首先执行 try 中的代码块，如果执行过程中出现异常，系统会自动生成一个异常类型，并将该异常提交给 Python 解释器，
          此过程称为<捕获异常>
        - 当 Python 解释器收到异常对象时，会寻找能处理该异常对象的 except 块，如果找到合适的 except 块，则把该异常对
          象交给该 except 块处理，这个过程被称为<处理异常>。如果 Python 解释器找不到处理异常的 except 块，则程序运行
          终止，Python 解释器也将退出。
        - 事实上，不管程序代码块是否处于 try 块中还是 except 块中的代码，只要执行该代码块时出现了异常，系统都会
          自动生成对应类型的异常。但是，如果此段程序没有用 try 包裹，又或者没有为该异常配置处理它的 except 块，则 Python 
          解释器将无法处理，程序就会停止运行；反之，如果程序发生的异常经 try 捕获并由 except 处理完成，则程序可以继续执行。
    """
    try:
        """
        @ socket
          1.定义：socket 又称为套接字，一个套接字就是网络上进程通信的一端，提供了应用层进程利用网络协议交换数据的机制
          2.作用：
            应用程序通常通过"套接字"向网络发出请求或者应答网络请求，使主机间或者一台计算机上的进程间可以通讯，即用于进
            程间通信
          3.表示方法：
            套接字Socket=(IP地址：端口号)，套接字的表示方法是点分十进制的lP地址后面写上端口号，中间用冒号或逗号隔开。
            每一个传输层连接唯一地被通信两端的两个端点（即两个套接字）所确定。
            例如：如果IP地址是210.37.145.1，而端口号是23，那么得到套接字就是(210.37.145.1:23)
          4.创建套接字
            socket.socket([family[, type[, proto]]])
                - family: 套接字家族可以是 AF_UNIX 或者 AF_INET
                    - AF_UNIX 用于同一台机器上的进程间通信
                    - AF_INET 用于 IPV4 协议的 TCP 和 UDP 
                - type: 套接字类型可以根据是面向连接的还是非连接分为 SOCK_STREAM 或 SOCK_DGRAM
                         [参考](https://www.jianshu.com/p/046f37121259)
                    - SOCK_STREAM 流套接字（TCP）
                    - SOCK_DGRAM 数据报文套接字（UDP）
                - protocol: 一般不填默认为 0
        """
        # 创建一个套接字 socket 赋值给变量 sock
        sock = socket.socket()
        # 设置当前 socket 实例连接或接收的超时时间为 3s
        sock.settimeout(3)
        """
        @ connect()
          1.定义：客户端套接字对象的内置方法 connect()
          2.说明：该方法会主动初始化 TCP 服务器连接，一般目标 address 的格式为元组 (hostname,port)
                  这里设置为目标 IP 和端口，如果连接出错，返回 socket.error 错误，如果该端口是开放的，
                  操作系统就能完成 TCP 三次握手，代码会继续执行
        """
        sock.connect((TargetIp, Port))
        # 关闭建立的连接，防止拒绝服务攻击
        sock.close()
        # 格式化输出，f 和 格式化字符串 format.str()类似，由大括号包含的变量和表达式会被传入的参数替换
        print(f"IP:{TargetIp} Port:{Port} --- open ")
        # 如果捕获的异常相匹配，将执行 Exception 里面的代码，此处表示所有异常，异常消息会传递给定义的变量 error
    except Exception as error:
        # showerror 初始值为 False, 如果布尔变量 showerror 的值为 True，将执行 print 语句
        if showerror:
            print(error)
        # 当 showerror 为假时，忽略该异常
        else:
            pass
    # 变量 pool_sema 调用 thread 库中的 release 方法，释放信号量
    pool_sema.release()


"""
@ __name__
程序入口，__name__ 是 python 中一个特别的属性，如果当前值为 __main__ 会执行 main 函数中包含的代码
"""
if __name__ == "__main__":
    # 打印扫描器脚本的版本信息
    print("pscan version 1.0")
    """
    @ sys.argv
      1.sys.argv 是一个 python 列表，用于保存从程序外部获取的参数
      2.特别注意 sys.argv[0] 表示的是程序本身，如本程序 juliao.py 运行时打印 sys.argv[0] 时的输出结果为 juliao.py
    """
    # 如果用户传入的参数个数没有 2 个，提示用户按正确的格式使用脚本，即需要传入参数目标 IP
    if len(sys.argv) != 2:
        # 传入的参数个数不为 2 时，打印此脚本的使用提示
        print(f"Usage:{sys.argv[0]} [TargetIp]")
        # 退出整个程序
        exit(0)
    # 创建一个名为 ThreadList 的列表
    ThreadList = []
    """
    @ range()
      1.原型 range(start, stop[, step])
        - start: 计数从 start 开始， 默认是从 0 开始。例如 range(5) 等价于 range(0, 5);
        - stop: 计数到 stop 结束，但不包括 stop。例如：range(0, 5) 是 [0, 1, 2, 3, 4] 没有 5        
        - step: 步长，默认为 1。例如：range(0, 5) 等价于 range(0, 5, 1)
      2.range(n), 表示的是将顺序生成从 0 到 n-1 之间的数，默认步长间隔为 1
      3.python3 中 range() 函数生成的是可迭代对象，不是列表
    """
    # 定义变量 i，i 的值从 0 到 9999，循环执行 10000 次，端口从 0-9999 之间进行扫描
    for i in range(10000):
        # 定义一个线程对象 ThreadObject 并对其进行初始化
        """
        @ __init__
          1.target: 将要被线程执行的对象，此时 ScannerThread 将成为一个被线程执行的函数（线程函数）
          2.args: 被调用对象的参数元组，这些参数将传入到 target 中去，此处传递了两个参数 sys.argv[1](IP), i(Port)
        """
        ThreadObject = threading.Thread(target=ScannerThread, args=(sys.argv[1], i))
        # 线程初始化，并且将线程对象传递给ThreadObject 如果不再用线程 会出现阻塞等等现象 而且扫描时间大大增加
        # 设置ScannerThread为线程函数
        # args 为传递给ScannerThread的参数 分别为：sys.argv 也就是第一个参数地址  第二个为i也就是端口
        """
        @ setDaemon()
          1.默认值是False，此时只有当子线程结束之后，主线程才会退出，
          2.设置为True时，就相当于是守护线程，该线程进入后台工作，可以把其想为不是很重要的线程。
            当主线程结束之后，不管子线程是否结束，子线程都会随着主线程的结束而被强制停止回收。
            这样的意义在于：
            - 避免了子线程出现死循环而导致整个程序无法退出
            - 避免出现主进程结束后，还需要逐个检查后台进程并关闭的情况
            - 避免出现孤儿进程的现象
        """
        ThreadObject.setDaemon(True)
        # 将初始化好的线程对象加入到列表 ThreadList 中去
        ThreadList.append(ThreadObject)
        # 原作者为了后面使用同样的命名变量函数不会起冲突而删除了 ThreadObject
        # 实际上在后面 for 循环进行变量时 ThreadObject 的值会被重新覆盖，不会冲突
    del ThreadObject
    # 使用变量 ThreadObject 来循环线程对象列表 ThreadList
    for ThreadObject in ThreadList:
        """
        @ start()
          Thread.start() 方法是 Python 中线程模块的 Thread 类的内置方法。
          它用于启动线程的活动。此方法在内部调用 run() 方法，然后执行目标方法。
          对于一个线程，此方法最多只能调用一次。如果它被多次调用，则会引发 RuntimeError
        """
        ThreadObject.start()
    # 原作者为了后面使用同样的命名变量函数不会起冲突而删除了 ThreadObject
    del ThreadObject
    # 使用变量 ThreadObject 来循环线程对象列表 ThreadList
    for ThreadObject in ThreadList:
        """
        @ join()
          1.语法格式：thread.join( [timeout] )
            - thread 为 Thread 类或其子类的实例化对象；
            - timeout 参数作为可选参数，其功能是指定 thread 线程最多可以霸占 CPU 资源的时间（以秒为单位）
              如果省略，则默认直到 thread 执行结束（进入死亡状态）才释放 CPU 资源。
          2.join() 方法的功能是在程序指定位置，优先让该方法的调用者使用 CPU 资源
        """
        ThreadObject.join()
    # 原作者为了后面使用同样的命名变量函数不会起冲突而删除了 ThreadObject
    del ThreadObject
    # 线程执行完后打印扫面完成消息
    print("PSCAN SUCCESSFULLY")
