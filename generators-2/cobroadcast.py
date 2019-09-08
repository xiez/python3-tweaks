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
    follow(f,
           broadcast([
               grep('python', printer()),
               grep('ply', printer()),
               grep('swig', printer()),
           ]))
