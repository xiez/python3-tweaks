import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from inlined_future3 import run_inline_future, start_inline_future, inlined_future

def run_inline_thread(gen):
    value = None
    exc = None
    while True:
        try:
            if exc:
                fut = gen.throw(exc)
            else:
                fut = gen.send(value)
            try:
                value = fut.result()
                exc = None
            except Exception as e:
                exc = e
        except StopIteration as exc:
            return exc.value

def fib(n):
    return 1 if n <= 2 else (fib(n-1) + fib(n-2))

@inlined_future
def compute_fibs(n):
    result = []
    for i in range(n):
        print(threading.current_thread())
        val = yield from pool.submit(fib, i)
        result.append(val)
    return result

pool = ProcessPoolExecutor(4)
tpool = ThreadPoolExecutor(8)

import time

# t0 = time.time()
# result = run_inline_future(compute_fibs(34))
# result = run_inline_future(compute_fibs(34))
# print(f"Time: {time.time() - t0}")

t0 = time.time()

t1 = tpool.submit(run_inline_thread, compute_fibs(34))
t2 = tpool.submit(run_inline_thread, compute_fibs(34))
print('---------')
print(t1.result())
print(t2.result())
print('---------')

print(f'Time2: {time.time() - t0}')
