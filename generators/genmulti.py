import threading
import queue
from genqueue import genfrom_queue, sendto_queue
from files import gen_cat
from tail import follow
from parser import apache_log

def multiplex(sources):
    in_q = queue.Queue()
    consumers = []
    for src in sources:
        thr = threading.Thread(target=sendto_queue, args=(src, in_q))
        thr.start()
        consumers.append(genfrom_queue(in_q))
    return gen_cat(consumers)

def print_r404(log):
    r404 = (r for r in log if r['status'] == 404)
    for r in r404:
        print(r['host'], r['datetime'], r['request'])

if __name__ == '__main__':
    lines = follow(open('www/access-log'))
    log = apache_log(lines)

    lines2 = follow(open('www/access-log'))
    log2 = apache_log(lines2)

    print_r404(multiplex([log, log2]))
