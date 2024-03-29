import socket

def receive_messages(addr, maxsize):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        msg = s.recvfrom(maxsize)
        yield msg

if __name__ == "__main__":
    for msg, addr in receive_messages(("", 10000), 10):
        print(msg, "from", addr)
