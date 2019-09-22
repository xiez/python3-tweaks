from concurrent.futures import ThreadPoolExecutor

def func(x, y):
    import time
    time.sleep(1)
    return x + y

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=8)

    def block():
        print('blocking...')
        fut = pool.submit(func, 2, 3)
        r = fut.result()
        print('Got: ', r)

    def block_with_exception():
        print('block with exception...')
        fut = pool.submit(func, 2, '3')
        try:
            r = fut.result()
        except Exception as e:
            print(f'Failed: {type(e).__name__}: {e}')

    def unblock():
        print('unblocking...')
        fut = pool.submit(func, 2, 3)
        fut.add_done_callback(unblock_handler)

    def unblock_with_exception():
        print('unblocking with exception...')
        fut = pool.submit(func, 2, '3')
        fut.add_done_callback(unblock_handler)

    def unblock_handler(fut):
        try:
            result = fut.result()
            print('Got:', result)
        except Exception as e:
            print(f'Failed: {type(e).__name__}: {e}')

    block()
    block_with_exception()
    unblock()
    unblock_with_exception()

    print('main done')
