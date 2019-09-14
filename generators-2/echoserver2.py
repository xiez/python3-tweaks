from socket import *
from pyos5 import NewTask
from pyos7 import ReadWait, WriteWait
from pyos8 import Scheduler, Accept, Send, Recv
from sockwrap import Socket

def handle_client(client, addr):
    print(f"Connection from {addr}")

    while True:
        data = yield client.recv(65536)
        if not data:
            break

        yield client.send(data)

    print("Client closed")
    client.close()

def server(port):
    print("Server starting")
    rawsock = socket(AF_INET, SOCK_STREAM)
    rawsock.bind(("", port))
    rawsock.listen(5)
    sock = Socket(rawsock)
    while True:
        client, addr = yield sock.accept()
        yield NewTask(handle_client(client, addr))

if __name__ == '__main__':
    def alive():
        while True:
            print('Im alive')
            yield

    sched = Scheduler()
    # sched.new(alive())
    sched.new(server(45000))
    sched.mainloop()
