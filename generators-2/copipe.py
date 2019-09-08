from coroutine import coroutine
from cofollow import follow, printer

@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)

if __name__ == '__main__':
    f = open('www/access-log')
    follow(f,
           grep('python',
                printer()))
