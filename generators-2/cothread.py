from queue import Queue
from threading import Thread, Lock
import xml.sax

from coroutine import coroutine
from cosax import EventHandler
from buses import buses_to_dicts, filter_on_field, bus_locations

lock = Lock()

@coroutine
def threaded(target):
    messages = Queue()

    def run_target():
        while True:
            item = messages.get()
            if item is GeneratorExit:
                target.close()
                return
            else:
                target.send(item)

    Thread(target=run_target).start()
    try:
        while True:
            item = (yield)
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)

@coroutine
def threaded_safe(target):
    """ref: https://anandology.com/blog/using-iterators-and-generators/"""
    messages = Queue()

    def run_target():
        while True:
            item = messages.get()
            with lock:
                if item is GeneratorExit:
                    target.close()
                    return
                else:
                    target.send(item)

    Thread(target=run_target).start()
    try:
        while True:
            item = (yield)
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)


if __name__ == '__main__':
    xml.sax.parse('allroutes.xml', EventHandler(
        buses_to_dicts(
            threaded(
                filter_on_field("route", "22",
                                filter_on_field("direction", "North Bound",
                                                bus_locations()))
            )
        )))
