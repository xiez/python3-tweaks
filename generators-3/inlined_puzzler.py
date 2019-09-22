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

    def after1(delay, gen):
        yield pool.submit(time.sleep, delay)
        yield gen

    def after2(delay, gen):
        yield pool.submit(time.sleep, delay)
        for f in gen:
            yield f

    def after3(delay, gen):
        yield pool.submit(time.sleep, delay)
        result = None
        try:
            while True:
                f = gen.send(result)
                result = yield f
        except StopIteration:
            pass

    def after4(delay, gen):
        yield pool.submit(time.sleep, delay)
        yield from gen

    # Task(after1(3, do_func(2, 3))).step()
    # Task(after2(3, do_func(2, 3))).step()
    # Task(after3(3, do_func(2, 3))).step()
    Task(after4(3, do_func(2, 3))).step()

    time.sleep(30)

    print('main done')
