from collections import deque
from functools import wraps
from queue import Queue
import threading
import time

_registry = {}
_msg_queue = deque()

def actor(func):
    @wraps(func)
    def wrapper(*args, id=func.__name__, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        _registry[id] = gen
    return wrapper

def send(name, msg):
    _msg_queue.append((name, msg))

def run():
    while _msg_queue:
        name, msg = _msg_queue.popleft()
        _registry[name].send(msg)

@actor
def ping():
    while True:
        n = yield
        print(f'ping {n}')
        send('pong', n + 1)
        time.sleep(1)

@actor
def pong():
    while True:
        n = yield
        print(f'pong {n}')
        send('ping', n + 1)

if __name__ == '__main__':
    ping()
    pong()

    send('ping', 1)

    run()
