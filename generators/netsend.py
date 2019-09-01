import socket
import pickle

from broadcast import broadcast
from parser import apache_log
from tail import follow

class NetConsumer:
    def __init__(self, addr):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(addr)

    def send(self, item):
        pitem = pickle.dumps(item)
        self.s.sendall(pitem)

    def close(self):
        self.s.close()


class Stat404(NetConsumer):
    def send(self, item):
        if item['status'] == 404:
            NetConsumer.send(self, item)

class LogConsumer(NetConsumer):
    def send(self, item):
        NetConsumer.send(self, item)

if __name__ == '__main__':
    lines = follow(open('www/access-log'))
    log = apache_log(lines)

    stat404 = Stat404(('', 15000))
    log_c = LogConsumer(('', 15001))
    broadcast(log, [stat404, log_c])
