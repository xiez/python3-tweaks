from actor1 import actor, send
import time, random

@actor
def ping():
    while True:
        n = yield
        print(f'ping {n}')
        send('pong', n + 1)

@actor
def pong():
    while True:
        n = yield
        print(f'pong {n}')
        send('ping', n + 1)

if __name__ == '__main__':
    ping()
    pong()
    send('ping', 0)
