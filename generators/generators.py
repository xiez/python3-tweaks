def countdown(start):
    print("Counting down from ", start)

    while start > 0:
        yield start
        start -= 1

def squares(l):
    return (x * x for x in l)

if __name__ == '__main__':
    g = squares([1, 2, 3])
    for i in g:
        print(i)
