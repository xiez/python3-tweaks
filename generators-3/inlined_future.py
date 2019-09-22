'''
@inlined_future
def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print('Got:', result)

run_inline_future(do_func)
'''

class Task:
    def __init__(self, gen):
        self._gen = gen
        self._is_finished = None

    def is_finished(self):
        return self._is_finished == True

    def join(self):
        while self._is_finished is not True:
            import time
            time.sleep(0.5)

    def step(self, value=None):
        print('step val:', repr(value))
        try:
            print('send value, ', value)
            fut = self._gen.send(value)
            print('fut', fut)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            print('Stop iteration')
            self._is_finished = True
            pass
        print('end step')

    def _wakeup(self, fut):
        print(f'wakeup fut:', fut)
        result = fut.result()
        self.step(result)

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import time

    pool = ThreadPoolExecutor(max_workers=3)

    def func(x, y):
        time.sleep(1)
        return x + y

    def do_func(x, y):
        print('before submit')
        result = yield pool.submit(func, x, y)
        print('after submit')
        print(f'Got: {result}')

    def do_many(n, val):
        while n > 0:
            result = yield pool.submit(func, n, val)
            print(f'Got: {result}')
            n -= 1

            time.sleep(0.1)

    # t = Task(do_func(2, 3))
    # t.step()

    t = Task(do_many(3, '1'))
    t.step()

    t2 = Task(do_many(3, 2))
    t2.step()

    # while not t.is_finished():
    #     time.sleep(0.5)

    t.join()
    t2.join()

    print('main done')
