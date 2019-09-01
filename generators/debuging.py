import math

from tail import follow
from parser import apache_log

def generate(func):
    def gen_func(s):
        for item in s:
            yield func(item)

    return gen_func

def trace(source):
    for item in source:
        print(item)
        yield item

class storelast:
    def __init__(self, source):
        self.source = source

    def __next__(self):
        item = self.source.__next__()
        self.last = item
        return item

    def __iter__(self):
        return self

if __name__ == '__main__':
    gen_sqrt = generate(math.sqrt)

    for x in trace(gen_sqrt(range(10))):
        pass

    print('--------------------')

    lines = storelast(follow(open('www/access-log')))
    log = apache_log(lines)
    for r in log:
        print(r)
        print(lines.last)
