import pickle
from multiprocessing import Process, Pipe
import xml.sax

from coroutine import coroutine
from cosax import EventHandler
from buses import buses_to_dicts, filter_on_field, bus_locations

@coroutine
def sendto(conn):
    try:
        while True:
            item = (yield)
            conn.send(item)
            # pickle.dump(item, f)
            # f.flush()
    except StopIteration:
        print('stop iteration')
        # f.close()
        conn.close()
    except GeneratorExit:
        print('sendto exit!')
        conn.send(GeneratorExit)

def recvfrom(conn, target):
    try:
        while True:
            item = conn.recv()
            if item is GeneratorExit:
                target.close()
                return

            # item = pickle.load(f)
            target.send(item)
    except EOFError:
        print('eof error')
        target.close()


if __name__ == '__main__':
    write_conn, read_conn = Pipe()

    p = Process(target=recvfrom, args=(
        read_conn,
        filter_on_field("route", "22",
                        filter_on_field("direction", "North Bound",
                                        bus_locations()))
    ))
    p.start()

    xml.sax.parse('allroutes.xml', EventHandler(
        buses_to_dicts(sendto(write_conn))
    ))

    print('======== done.')
