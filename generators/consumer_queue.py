import threading
import queue
from genqueue import genfrom_queue, sendto_queue
from tail import follow
from parser import apache_log

def print_r404(log_q):
    log = genfrom_queue(log_q)
    print('genfrom_queue: ', log)
    r404 = (r for r in log if r['status'] == 404)
    for r in r404:
        print(r['host'], r['datetime'], r['request'])

def feed_queue(log_q):
    lines = open('www/access-log')
    lines = follow(lines)
    log = apache_log(lines)
    sendto_queue(log, log_q)

if __name__ == '__main__':
    log_q = queue.Queue()
    r404_thr = threading.Thread(target=print_r404, args=(log_q,))
    r404_thr.start()
    print('start consumer thread.')

    feed_thr = threading.Thread(target=feed_queue, args=(log_q,))
    feed_thr.start()
    print('start producer thread.')
