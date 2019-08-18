from pathlib import Path
import bz2
import gzip
import re

def gen_open(paths):
    for path in paths:
        if path.suffix == '.gz':
            yield gzip.open(path, 'rt')
        elif path.suffix == '.bz2':
            yield bz2.open(path, 'rt')
        else:
            yield open(path, 'rt')

def gen_cat(sources):
    for src in sources:
        yield from src

def gen_match(pat, lines):
    patc = re.compile(pat)
    return (patc.match(line) for line in lines)

def gen_groups(matches):
    return (m.groups() for m in matches if m)

def gen_dicts(colnames, groups):
    return (dict(zip(colnames, g)) for g in groups)

def field_map(dictseq, name, func):
    for d in dictseq:
        d[name] = func(d[name])
        yield d

# general purpose component ##########
def lines_from_dir(dirname, filepat):
    lognames = Path(dirname).rglob(filepat)
    logfiles = gen_open(lognames)
    loglines = gen_cat(logfiles)
    return loglines

def apache_log(lines, logpat=None):
    if not logpat:
        logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\S+) (\S+)'

    matches = gen_match(logpats, lines)
    groups = gen_groups(matches)
    colnames = ('host', 'referer', 'user', 'datetime', 'method', 'request',
                'proto', 'status', 'bytes')
    log = gen_dicts(colnames, groups)

    log = field_map(log, 'status', int)
    log = field_map(log, 'bytes', lambda s: int(s) if s != '-' else 0)
    return log
# END general purpose component ##########

if __name__ == '__main__':
    lines = lines_from_dir('www', 'access-log*')
    logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\S+) (\S+)'
    log = apache_log(lines, logpats)

    # print(max((r['bytes'], r['request']) for r in log))

    # hosts = { r['host'] for r in log if 'robots.txt' in r['request']}
    # print(hosts)
    # import socket
    # for addr in hosts:
    #     try:
    #         print(socket.gethostbyaddr(addr)[0])
    #     except socket.herror:
    #         print(addr)

    total_requests = 0
    total_bytes = 0
    total_200 = 0
    total_3xx = 0
    total_4xx = 0
    total_5xx = 0
    for d in log:

        if d['status'] == 200:
            total_200 += 1
        elif d['status'] >= 300 and d['status'] < 400:
            total_3xx += 1
        elif d['status'] >= 400 and d['status'] < 500:
            total_4xx += 1
        elif d['status'] >= 500 and d['status'] < 600:
            total_5xx += 1

        total_requests += 1
        total_bytes += d['bytes']

    print('Total requests: ', total_requests)
    print('           200: ', total_200)
    print('           3xx: ', total_3xx)
    print('           4xx: ', total_4xx)
    print('           5xx: ', total_5xx)
    print('Total bytes(MB): {:.2f}'.format(total_bytes / 1024 / 1024))
