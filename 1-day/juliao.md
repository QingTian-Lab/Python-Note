> Python Note  
> @ Juliao 

# Day 01
阅读代码并添加注释

# Day 02
重构 AAportscan.py 脚本  

端口扫描的现有方案原理：
- TCP 三次握手
- SYN 半开放式扫描

结合线程：
- 单线程
- 多线程

伪代码：

```python
import socket
import our_libs

# 定义全局变量接受用户自定义IP、Port范围
ip = input_ip
port = input_port
...

# 创建端口扫描函数，通过socket套接字建立TCP请求
# 如果和制定的IP及端口成功建立握手，说明端口开放
# 打印开放的端口，否则抛出异常
def port_scanner(ip, port):
    try:
        sock = socket.socket()
        if sock:
            print(ip + port + "is open!")
        else:
    except Exception as e:
        print("error")

# 创建处理扫描函数的线程，并定义处理逻辑
def thread_handler():
    # 创建线程对象
    thread_object
    # 线程的获取
    thread.aquire()
    # 让port_scanner成为线程处理对象
    thread_object(port_scanner())
    # 线程开始
    thread_object.start()
    # 守护线程
    thead.setDaemon()
    # 释放线程
    thread.release()
    
# 主程序入口
if __name__ == "__main__":
    thread_handler()
```

