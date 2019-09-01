import time
import threading

from tail import follow

shutdown = threading.Event()
lines = follow(open('www/access-log'), shutdown)

def sleep_and_close(s):
    time.sleep(s)
    print('Closing it down')
    shutdown.set()

threading.Thread(target=sleep_and_close, args=(10,)).start()

for line in lines:
    print(line, end='')
