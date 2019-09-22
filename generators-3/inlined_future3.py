'''
@inlined_future
def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print('Got:', result)

run_inline_future(do_func)
'''
from concurrent.futures import Future
import inspect

def patch_future(cls):
    def __iter__(self):
        if not self.done():
            yield self
        return self.result()
    cls.__iter__ = __iter__

patch_future(Future)


class Task(Future):
    def __init__(self, gen):
        super().__init__()
        self._gen = gen

    def step(self, value=None, exc=None):
        print('step val:', repr(value))
        try:
            if exc:
                print('throw exc, ', exc)
                fut = self._gen.throw(exc)
            else:
                print('send value, ', value)
                fut = self._gen.send(value)
            print('fut', fut)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            print('Stop iteration')
            print(f'exc value: {exc.value}')
            self.set_result(exc.value)

        print('end step')

    def _wakeup(self, fut):
        print(f'wakeup fut:', fut)
        try:
            result = fut.result()
            self.step(result, None)
        except Exception as exc:
            self.step(None, exc)

def inlined_future(func):
    assert inspect.isgeneratorfunction(func)
    return func

def start_inline_future(fut):
    t = Task(fut)
    t.step()
    return t

def run_inline_future(fut):
    t = start_inline_future(fut)
    return t.result()

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import time

    pool = ThreadPoolExecutor(max_workers=3)

    def func(x, y):
        time.sleep(1)
        return x + y

    @inlined_future
    def do_func(x, y):
        print('before submit')
        result = yield pool.submit(func, x, y)
        print('after submit')
        print(f'Got: {result}')
        return result

    @inlined_future
    def after(delay, gen):
        yield from pool.submit(time.sleep, delay)
        result = yield from gen
        return result

    # t = Task(after(3, do_func(2, 3)))
    # t.step()
    # print(f'Got: {t.result()}')

    # result = run_inline_future(do_func(2, 3))
    # print(f'Got: {result}')

    t1 = start_inline_future(do_func(2, 3))
    t2 = start_inline_future(after(5, do_func(3, 4)))

    print(f'Got result: {t1.result()}')
    print(f'Got result: {t2.result()}')

    print('main done')
