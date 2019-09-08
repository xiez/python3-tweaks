from coroutine import coroutine
from cofollow import follow, printer
from copipe import grep

@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)

if __name__ == '__main__':
    f = open('www/access-log')
    p = printer()
    follow(f,
           broadcast([
               grep('python', p),
               grep('ply', p),
               grep('swig', p),
           ]))
