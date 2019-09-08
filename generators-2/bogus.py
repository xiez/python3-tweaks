def countdown(n):
    print(f'Counting down from {n}')

    while n >= 0:
        newvalue = (yield n)
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1

        import time
        time.sleep(2)

c = countdown(5)
for n in c:
    print(n)
    if n == 5:
        c.send(3)
