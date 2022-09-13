import sys
import threading
import queue
import socket
q = queue.Queue() # 创建一个队列q
class Portscanner(threading.Thread): # 新建一个名为Portscanner的类，该类继承Thread类
    def __init__(self,host):   # 初始化属性值 host,后面所有需要用到host值的地方都会调用它
        super().__init__()  #super()函数是将父类和子类关联起来，让Portscnner实例包含父类的所有属性
        self.host: str = host # 初始化host值，
    def run(self) -> None: # 该函数为目标函数，即定义线程后的执行函数
        while True:
            port = q.get() #将main方法中通过put()方法加入队列中的值在while循环中一个一个取出来，赋值给变量port
            self.scanner(port)  # 将变量port中的值带入到函数scanner中，调用并执行scanner函数
            q.task_done()  # 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号。每个get()调用得到一个任务，接下来task_done()调用告诉队列该任务已经处理完毕
    def scanner(self,port):
        conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 新建一个socket
        try:
            conn.connect((self.host,port)) # 使用套接字建立连接
            print(f'[+] {port} is open')    # 若连接成功，则打印此段话
        except:  # 除非连接成功，其余所有报错全部pass
            pass
if __name__ == '__main__':
    host = sys.argv[1]
    ip = socket.gethostbyname(host) # 若用户输入的是域名，则通过此方法将域名转换为IP地址，若是IP地址则不影响
    startPort = sys.argv[2]
    endPort = sys.argv[3]
    threadNum = sys.argv[4]
    for i in range(int(startPort),int(endPort)): # 根据用户输入的第二个和第三个值确定要扫描的端口区间
        q.put(i)   # 将要扫描的端口加入到队列中
    for i in range(int(threadNum)):  # 根据用户输入的值开启对应的线程
        # 定义一个多线程，因为新类Portscanner中，继承了Thread类，所以不用像以前那样 threading.Thread(target=**,args=**)
        # 这里直接调用新类Portscanner(),它自动去找新类中得run()方法，并运行，该方法为目标函数
        t = Portscanner(ip)
        t.setDaemon(True)  # 设置守护线程，即主线程结束后，所有子线程立即结束。
        t.start()  # 开启线程
    q.join()  # 等待所有队列执行结束



