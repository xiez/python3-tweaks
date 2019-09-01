import sys

from receivefrom import receivefrom

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 netrecv.py 0.0.0.0 15000')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    for r in receivefrom((host, port)):
        print(r)
