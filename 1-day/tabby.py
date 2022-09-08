import sys
import socket
import threading

# 这里的showerror这个变量被定义为了一个布尔值
showerror = True

# pool_sema是变量名，他的值是threading库里的BoundedSemaphore方法，该方法的值被设置为了 1000
pool_sema = threading.BoundedSemaphore(1000)

# def意思是定义一个函数，ScannerThread是函数名，TargetIp和Port=80是定义该函数的编程者自己定义的参数
def ScannerThread(TargetIp, Port=80):

    # 代表调用 pool_sema 变量所代表threading库里面的的BoundedSemaphore函数里面acquire方法，具体功能需要了解acquire方法的功能
    pool_sema.acquire()  # 线程数 的锁 忽略

    # try代表了异常处理，解释器看到这个会按照:后面的代码块内的定义的异常处理进行异常处理
    try: # 异常处理头

        # 定义一个名为sock的变量，他的值是socket库里面的socket()函数，该函数作用是建立一条sockset
        sock = socket.socket() # 初始化一个socket，并且传递给sock

        # sock已经代表一条socket了，此时编程者调用socket.socket()函数里面的settimeout方法，功能是设置socket会话超时时间
        sock.settimeout(3) # 设置超时时间

        # 编程者调用socket.socket()内的connect方法对定义的TargetIp，Port发起TCP connect连接，ps: connect方法会完成三次握手才算成功。
        sock.connect((TargetIp, Port))  # 进行TCP连接，如果成功连接代表端口开放会继续执行。但是如果失败代表端口不开放，该函数会抛出异常信息

        # 编程者调用同上的函数调用close方法，该方法功能是关闭tcp连接会话
        sock.close() #释放连接

        # print函数向标准输出输出字符，f不理解是什么意思，TargetIp是变量，应该是由用户输入传入的但逻辑目前还没出现
        # 其实无论扫没有扫到开放端口，标准输出都是会显示socket状态的,这里只是定义了没有抛出异常的print也就是正常建立tcp连接的端口，如果不进行异常处理
        # 我们会看到关闭的端口将会显示socket库所定义的端口重置的消息，这个消息是库已经定义好的
        # 异常后的行为由43行控制，而43行又受第6行控制，所第6行实现的是debug功能
        print(f"IP:{TargetIp} Port:{Port} --- open ") # 通过格式化字符串输出开放信息

        # except 是异常处理内置关键字，他不是函数和方法也不是类，Exception是异常处理的类型，Exception代表了所有异常
    except Exception as error: # 异常处理 ,捕获Exception异常（在Python代表所有异常），并且将异常信息传递给error

        # 在第六行定义的showerror变量如果是True就是向标准输出输出打印错误信息
        if showerror == True: # 如果该值为True 会执行print(eror)
            print(error)

        # 否则就pass，pass表示什么都没发生，解释器继续向下执行，但是为什么会屏蔽错误输出不理解
        else: # 否则 不执行任何代码
            pass

    # 调用第九行定义的最大线程函数 threading.BoundedSemaphore(1000)的release方法，功能是释放线程锁
    pool_sema.release() # 线程数 的锁 忽略

# python解释器将从这里开始对代码解释运行
# 此处不理解为什么不从第一行运行，什么情况下不会从第一行运行，双下划线__也不知道是什么意思
if __name__ == "__main__":

    # 打印pscan version 1.0 等版本信息字符
    print("pscan version 1.0")

    # 如果 sys库里的argv函数的值现在不等于2，也就是如果执行脚本对时候传入的参数不是两个的话就执行下一段if代码块的缩进语句
    if len(sys.argv) != 2: # 通过判断参数数量来识别是否正确传递参数

        # 满足上一行就会执行打印 一个提示语，f不知道什么意思，sys.argv[0]是从左往右第一个参数，也就是文件名（数的时候不含python3这句）
        # 例如"python3 scan.py 1.1.1.1" sys.argv[0]是scan.py sys.argv[1] 是1.1.1.1
        print(f"Usage:{sys.argv[0]} [TargetIp]") # 数量不符合将执行此代码

        # 然后退出，如果不满足if的条件，解释器将不会执行到这里
        exit(0) # 退出程序

    # 创建一个变量，他的值是一个列表，目前这个列表是空的，但他不是null
    ThreadList = []

    # 创建一个for循环，i 将被range函数赋值10000次，range函数的值就是他的功能和参数决定的，
    # 功能是创建一个整数序列，参数是10000，那就是创建10000个整数
    for i in range(10000): # 循环10000次，并且传递给i 也就是从0到10000端口进行扫描

        # 定义一个ThreadObject变量，他的值是threading库里面的Thread函数(IDE表示Thread是一个class类)
        # target=ScannerThread表示target参数由ScannerThread传入，而ScannerThread是12行自定义的函数
        # args=(sys.argv[1], i)表示args参数由sys库argv参数传入[1]代表ip地址，正如59行解释。i表示for循环中的循环变量
        # 整体功能就是一个线程由编程者自定义的ScannerThread函数逻辑完成
        # Thread只负责创建线程，（）里面的参数代表线程中需要干什么
        # 一个线程需要干的事情就是ScannerThread函数的功能定义加上参数sys.argv[1]也就是ip地址和端口传入ScannerThread函数完成一个线程的功能
        # 最后面的i会被for循环循环执行，也就是循环替换i的值，反复的执行整个ThreadObject变量，直到下面的条件成立
        # 思考：sys.argv[1]是否可以换成 ScannerThread(TargetIp, i)达到同样功能
        # 整个循环会执行10000次 python3 tabby.py 192.168.1.1 i 10000次执行只有i会变动，也就是轮询端口
        ThreadObject = threading.Thread(target=ScannerThread, args=(sys.argv[1], i))  # 线程初始化，并且将线程对象传递给ThreadObject 如果不再用线程 会出现阻塞等等现象 而且扫描时间大大增加
        # 设置ScannerThread为线程函数
        # args 为传递给ScannerThread的参数 分别为：sys.argv 也就是第一个参数地址  第二个为i也就是端口

        # 此时还未退出for循环,调用ThreadObject对象的setDaemon方法，值是True，功能是开启守护线程
        ThreadObject.setDaemon(True) # 设置守护线程 如果主线程崩了 别的线程一起中断执行

        # 67行定义的空列表在此时会被加入值，提前定义是为了保留这个列表，方便此时此刻调用，如果在for循环里面定义，列表将会被定义10000次
        # ThreadObject对象被添加传入ThreadList定义的列表，列表里面储存的是线程任务，并不是单次循环的执行结果
        ThreadList.append(ThreadObject) # 将线程对象加入到列表里

        # 71-91行的for循环只是为了创建线程任务传给一个列表，并没有任何的实质性功能

    # 删除ThreadObject这个对象，后面不定义将无法再次使用了，从缩进来看此时的代码已经脱离了for循环，for循环结束后才会删除ThreadObject这个对象
    del ThreadObject  # 删除ThradObject 这样后面使用同样的命名变量函数不会起冲突



    # 创建一个for循环，将ThreadList列表里面的对象轮询赋值给ThreadObject变量，从101行开始的ThreadObject变量已经是一个新变量，
    # 和101行以上的ThreadObject不是一个对象，因为在96行他被删除了，脚本语言遵循从上往下解释执行的原则
    for ThreadObject in ThreadList: # 循环线程对象列表

        # 真正的功能被调用了，此时列表里面储存的82行定义的线程对象被调用了start()方法，此时socket已经开始发包了
        ThreadObject.start() # 开启线程

    del ThreadObject # 删除变量

    # 再次创建一个for循环，将ThreadList列表（里面是线程对象，不是值）循环赋值给ThreadObject，此时的ThreadObject 是新定义的ThreadObject
    for ThreadObject in ThreadList: #循环线程对象列表

        # 循环调用ThreadObject对象里面的join方法，该方法功能不清楚
        ThreadObject.join() # 阻塞 通过它来保证主线程不会退出，通过循环每一个线程 join会以ScannerThread执行是否完成为条件进行阻塞

        # 再次删除ThreadObject对象
    del ThreadObject

    # 输出字符，扫描完成
    print("PSCAN SUCCESSFULLY")




