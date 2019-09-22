'''
@inlined_future
def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print('Got:', result)

run_inline_future(do_func)
'''
from inlined_future2 import Task


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import time

    pool = ThreadPoolExecutor(max_workers=3)

    def recursive(n):
        yield pool.submit(time.sleep, 1)
        print(f'Tick: {n}')
        Task(recursive(n + 1)).step()

    t = Task(recursive(0))
    t.step()

    while True:
        time.sleep(10)

    print('main done')
