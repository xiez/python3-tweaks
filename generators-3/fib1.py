import threading
from concurrent.futures import ProcessPoolExecutor

from inlined_future3 import run_inline_future, start_inline_future, inlined_future

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

import time

# t0 = time.time()
# run_inline_future(compute_fibs(34))
# run_inline_future(compute_fibs(34))
# print(f'Time: {time.time() - t0}')

t0 = time.time()
t1 = start_inline_future(compute_fibs(34))
t2 = start_inline_future(compute_fibs(34))
t1.result()
t2.result()
print(f'Time2: {time.time() - t0}')
