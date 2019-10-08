_registry = {}

def actor(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        _registry[func.__name__] = gen
    return wrapper

def send(name, msg):
    _registry[name].send(msg)

@actor
def printer():
    while True:
        msg = yield
        print(f'printer: {msg}')

if __name__ == '__main__':
    printer()
    print(_registry)

    n = 10
    while n > 0:
        send('printer', n)
        n -= 1
