# https://www.python.org/dev/peps/pep-0380/

def yield_from(expr):
    _i = iter(expr)
    try:
        _y = next(_i)
        print(f'_y: {_y}')
    except StopIteration as _e:
        _r = _e.value
        print(f'_r: {_r}')
    else:
        while 1:
            _s = yield _y
            print(f'_s: {_s}')

            try:
                if _s is None:
                    _y = next(_i)
                    print(f'_y: {_y}')
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:
                _r = _e.value
                break

    result = _r
    print(f'result: {result}')
    return result

def g():
    yield 1
    yield 2
    return 3
    # raise StopIteration(3)

def f():
    a = yield from g()
    print(a)

if __name__ == '__main__':
    for _ in yield_from(g()):
        pass

    print('----------')

    for _ in f():
        pass
