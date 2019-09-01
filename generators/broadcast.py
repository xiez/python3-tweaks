from tail import follow

def broadcast(source, consumers):
    for item in source:
        print('item: ', item)
        for c in consumers:
            c.send(item)

class Consumer:
    def send(self, item):
        print(self, "got", item)


if __name__ == '__main__':
    c1 = Consumer()
    c2 = Consumer()
    c3 = Consumer()

    lines = follow(open('www/access-log'))
    broadcast(lines, [c1, c2, c3])
