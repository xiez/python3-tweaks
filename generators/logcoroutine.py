from recvcount import consumer
from tail import follow
from parser import apache_log
from broadcast import broadcast

@consumer
def find_404():
    while True:
        r = yield
        if r['status'] == 404:
            print(r['status'], r['datetime'], r['request'])

@consumer
def bytes_transferred():
    total = 0
    while True:
        r = yield
        total += r['bytes']
        print('Total bytes', total)

if __name__ == '__main__':
    lines = follow(open('www/access-log'))
    log = apache_log(lines)

    broadcast(log, [find_404(), bytes_transferred()])
