def sendto_queue(source, thequeue):
    for item in source:
        thequeue.put(item)
    thequeue.put(StopIteration)

def genfrom_queue(thequeue):
    while True:
        item = thequeue.get()
        if item is StopIteration:
            break
        yield item
