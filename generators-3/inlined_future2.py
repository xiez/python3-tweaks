'''
@inlined_future
def do_func(x, y):
    result = yield pool.submit(func, x, y)
    print('Got:', result)

run_inline_future(do_func)
'''

DEBUG = False

def log(msg, debug=DEBUG):
    if not DEBUG:
        return
    else:
        print(msg)

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

    def step(self, value=None, exc=None):
        log('step val:', repr(value))
        try:
            if exc:
                log(f'throw exception: {exc}')
                fut = self._gen.throw(exc)
            else:
                log(f'send value: {value}')
                fut = self._gen.send(value)
            log(f'fut, {fut}')
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            log('Stop iteration')
            self._is_finished = True
            pass
        except Exception as exc:
            log('Boom!!!')
            self._is_finished = True

        log('end step')

    def _wakeup(self, fut):
        try:
            result = fut.result()
            self.step(result)
        except Exception as exc:
            self.step(None, exc)

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import time

    pool = ThreadPoolExecutor(max_workers=3)

    def func(x, y):
        time.sleep(1)
        return x + y

    def do_func(x, y):
        log('before submit')
        result = yield pool.submit(func, x, y)
        log('after submit')
        print(f'Got: {result}')

    def do_many(n, val):
        while n > 0:
            result = yield pool.submit(func, n, val)
            print(f'Got: {result}')
            n -= 1

            time.sleep(0.1)

    t = Task(do_many(3, '1'))
    t.step()

    t2 = Task(do_many(3, 1))
    t2.step()

    # while not t.is_finished():
    #     time.sleep(0.5)

    t.join()
    t2.join()

    log('main done')
