def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start

@coroutine
def grep(pattern):
    print(f"Looking for {pattern}")
    try:
        while True:
            line = (yield)
            if pattern in line:
                print(line)
    except RuntimeError as e:
        print(f'Got runtime error: {e}')
        # yield -1
        raise
    except GeneratorExit:
        print("Going away. Goodbye")
