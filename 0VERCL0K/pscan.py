import sys, socket, threading

showerror = False  # 连接异常信息输出
pool_sema = threading.BoundedSemaphore(1000) # 线程数限制  不限制会卡死


def ScannerThread(TargetIp, Port=80):
    pool_sema.acquire()  # 线程数 的锁 忽略
    try: # 异常处理头
        sock = socket.socket() # 初始化一个socket，并且传递给sock
        sock.settimeout(3) # 设置超时时间
        sock.connect((TargetIp, Port))  # 进行TCP连接，如果成功连接代表端口开放会继续执行。但是如果失败代表端口不开放，该函数会抛出异常信息
        sock.close() #释放连接
        print(f"IP:{TargetIp} Port:{Port} --- open ") # 通过格式化字符串输出开放信息
    except Exception as error: # 异常处理 ,捕获Exception异常（在Python代表所有异常），并且将异常信息传递给error
        if showerror: # 如果该值为True 会执行print(eror)
            print(error)
        else: # 否则 不执行任何代码
            pass
    pool_sema.release() # 线程数 的锁 忽略


if __name__ == "__main__":
    print("pscan version 1.0")
    if len(sys.argv) != 2: # 通过判断参数数量来识别是否正确传递参数
        print(f"Usage:{sys.argv[0]} [TargetIp]") # 数量不符合将执行此代码
        exit(0) # 退出程序
    ThreadList = []
    for i in range(10000): # 循环10000次，并且传递给i 也就是从0到10000端口进行扫描
        ThreadObject = threading.Thread(target=ScannerThread, args=(sys.argv[1], i))  # 线程初始化，并且将线程对象传递给ThreadObject 如果不再用线程 会出现阻塞等等现象 而且扫描时间大大增加
        # 设置ScannerThread为线程函数
        # args 为传递给ScannerThread的参数 分别为：sys.argv 也就是第一个参数地址  第二个为i也就是端口
        ThreadObject.setDaemon(True) # 设置守护线程 如果主线程崩了 别的线程一起中断执行
        ThreadList.append(ThreadObject) # 将线程对象加入到列表里
    del ThreadObject  # 删除ThradObject 这样后面使用同样的命名变量函数不会起冲突

    for ThreadObject in ThreadList: # 循环线程对象列表
        ThreadObject.start() # 开启线程
    del ThreadObject # 删除变量

    for ThreadObject in ThreadList: #循环线程对象列表
        ThreadObject.join() # 阻塞 通过它来保证主线程不会退出，通过循环每一个线程 join会以ScannerThread执行是否完成为条件进行阻塞
    del ThreadObject

    print("PSCAN SUCCESSFULLY")
