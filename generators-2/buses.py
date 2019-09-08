from coroutine import coroutine

@coroutine
def buses_to_dicts(target):
    while True:
        event, value = (yield)
        if event != 'start' or value[0] != 'bus':
            continue

        busdict = {}
        fragments = []
        while True:
            event, value = (yield)
            if event == 'start':
                fragments = []
            elif event == 'text':
                fragments.append(value)
            elif event == 'end':
                if value != 'bus':
                    busdict[value] = "".join(fragments)
                else:
                    target.send(busdict)
                    break

@coroutine
def filter_on_field(fieldname, value, target):
    while True:
        d = (yield)
        if d.get(fieldname) == value:
            target.send(d)

@coroutine
def bus_locations():
    while True:
        bus = (yield)
        print('bus -> ', bus)
