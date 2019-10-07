class StopIteration(Exception):

    def __init__(self, *args):
        if len(args) > 0:
            self.value = args[0]
        else:
            self.value = None
        Exception.__init__(self, *args)

if __name__ == '__main__':
    try:
        raise StopIteration(3)
    except StopIteration as e:
        print(f'StopIteration value: {e.value}')
