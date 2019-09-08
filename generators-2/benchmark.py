from coroutine import coroutine
from copipe import grep

class GrepHandler:
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def send(self, line):
        if self.pattern in line:
            self.target.send(line)

@coroutine
def null():
    while True:
        item = (yield)

line = 'python is nice'
p1 = grep('python', null())
p2 = GrepHandler('python', null())

'''Results:

➜  generators-2 git:(master) ✗ python -i benchmark.py
>>> from timeit import timeit
>>> timeit("p1.send(line)", "from __main__ import line,p1", number=10000000)
timeit("p1.send(line)", "from __main__ import line,p1", number=10000000)
1.9681993200000107
>>> timeit("p2.send(line)", "from __main__ import line,p2", number=10000000)
timeit("p2.send(line)", "from __main__ import line,p2", number=10000000)
2.5010494020000067
'''
