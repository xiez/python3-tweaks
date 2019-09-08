import xml.sax
from buses import buses_to_dicts, filter_on_field, bus_locations

class EventHandler(xml.sax.ContentHandler):
    def __init__(self, target):
        self.target = target

    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))

    def characters(self, text):
        self.target.send(('text', text))

    def endElement(self, name):
        self.target.send(('end', name))

if __name__ == '__main__':
    xml.sax.parse('allroutes.xml', EventHandler(
        buses_to_dicts(
            filter_on_field("route", "22",
                            filter_on_field("direction", "North Bound",
                                            bus_locations()))
        )))
