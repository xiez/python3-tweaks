import xml.parsers.expat
from buses import buses_to_dicts, filter_on_field, bus_locations

def expat_parse(f, target):
    parser = xml.parsers.expat.ParserCreate()
    parser.buffer_size = 65536
    parser.buffer_text = True
    # parser.returns_unicode = False
    parser.StartElementHandler = lambda name, attrs: target.send(('start', (name, attrs)))
    parser.EndElementHandler = lambda name: target.send(('end', name))
    parser.CharacterDataHandler = lambda data: target.send(('text', data))
    parser.ParseFile(f)

if __name__ == '__main__':
    expat_parse(open('allroutes.xml', 'rb'), buses_to_dicts(
        filter_on_field("route", "22",
                        filter_on_field("direction", "North Bound",
                                        bus_locations()))
    ))
