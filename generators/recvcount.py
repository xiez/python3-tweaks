def consumer(func):
    def start(*args, **kwargs):
        c = func(*args, **kwargs)
        c.send(None)
        return c
    return start

@consumer
def recv_count():
    print('recv_coun')
    try:
        while True:
            n = yield
            print("T-minus", n)
    except GeneratorExit:
        print("Kaboom!")
