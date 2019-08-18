import os
import time
from parser import apache_log

def follow(thefile):
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open('www/access-log')
    loglines = follow(logfile)
    log = apache_log(loglines)
    r404 = (r for r in log if r['status'] == 404)

    for r in r404:
        print(r['host'], r['datetime'], r['request'])
