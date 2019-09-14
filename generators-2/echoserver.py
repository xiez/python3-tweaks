from socket import *
from pyos5 import NewTask
from pyos7 import ReadWait, WriteWait
from pyos8 import Scheduler, Accept, Send, Recv

def handle_client(client, addr):
    print(f"Connection from {addr}")

    while True:
        data = yield Recv(client, 65536)
        if not data:
            break

        yield Send(client, data)

    print("Client closed")
    client.close()

def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        client, addr = yield Accept(sock)
        yield NewTask(handle_client(client, addr))

if __name__ == '__main__':
    def alive():
        while True:
            print('Im alive')
            yield

    sched = Scheduler()
    # sched.new(alive())
    sched.new(server(45001))
    sched.mainloop()
