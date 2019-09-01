def print_count(n):
    yield "Hello World\n"
    yield "\n"
    yield "Look at me count to %d\n" % n
    for i in range(n):
        yield "    %d\n" % i
    yield "I'm done!\n"


if __name__ == "__main__":
    out = print_count(10)
    out_str = "".join(out)
    print(out_str)

    print('------------------------------')

    out = print_count(10)
    f = open('out.txt', 'w')
    for chunk in out:
        f.write(chunk)
