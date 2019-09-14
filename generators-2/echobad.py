from socket import *
from pyos5 import NewTask
from pyos6 import Scheduler

def handle_client(client, addr):
    print(f"Connection from {addr}")

    while True:
        data = client.recv(65536)
        if not data:
            break
        client.send(data)

    client.close()
    print("Client closed")
    yield

def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))

if __name__ == '__main__':
    def alive():
        while True:
            print('Im alive')
            yield

    sched = Scheduler()
    sched.new(alive())
    sched.new(server(45000))
    sched.mainloop()
