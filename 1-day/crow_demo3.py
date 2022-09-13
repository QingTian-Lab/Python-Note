import sys
import threading
import socket
import queue
q = queue.Queue()

class Portscanner(threading.Thread):
    def __init__(self,host):
        super().__init__()
        self.host:str = host
    def run(self) -> None:
        while True:
            port = q.get()
            self.scanner(port)
            q.task_done()
    def scanner(self,port):
        try:
            socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect((self.host,port))
            print(f'[+] {port} is open')
        except:
            pass
if __name__ == '__main__':
    host = sys.argv[1]
    ip = socket.gethostbyname(host)
    stratPort = sys.argv[2]
    endPort = sys.argv[3]
    threadNum = sys.argv[4]
    for item in range(int(stratPort),int(endPort)):
        q.put(item)
    for i in range(int(threadNum)):
        t = Portscanner(ip)
        t.setDaemon(True)
        t.start()
    q.join()