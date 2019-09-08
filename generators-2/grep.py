def grep(pattern):
    print(f"Looking for {pattern}")
    while True:
        line = (yield)
        if pattern in line:
            print(line)
