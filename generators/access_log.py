def nongen():
    with open('www/access-log') as wwwlog:
        total = 0
        for line in wwwlog:
            bytes_sent = line.rsplit(None, 1)[1]
            if bytes_sent != '-':
                total += int(bytes_sent)
        print("Total", total)

def gen():
    with open('www/access-log') as wwwlog:
        bytecolumn = (line.rsplit(None, 1)[1] for line in wwwlog)
        bytes_sent = (int(x) for x in bytecolumn if x != '-')
        print("Total", sum(bytes_sent))

if __name__ == '__main__':
    print('--- non generator ---')
    nongen()

    print('--- generator ---')
    gen()
