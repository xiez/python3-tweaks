class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return CountdownIter(self.start)


class CountdownIter:
    def __init__(self, count):
        self.count = count

    def __next__(self):
        if self.count <= 0:
            raise StopIteration

        r = self.count
        self.count -= 1
        return r


if __name__ == '__main__':
    c = Countdown(10)

    print('-- count down -- ')
    for i in c:
        print(i, end=' ')

    print()
    print('-- under the hood -- ')

    _iter = iter(c)
    while 1:
        try:
            x = _iter.__next__()
            print(x, end=' ')
        except StopIteration:
            break

    print()
