import re
from pathlib import Path

def gen_ls(path, filename):
    pys = Path(path).rglob(filename)
    print(pys)
    for filename in pys:
        print(filename)
        yield filename

def gen_open(paths):
    for path in paths:
        yield open(path, 'rt')

def gen_cat(sources):
    for src in sources:
        yield from src

def gen_cat2(sources):
    for src in sources:
        # for no, line in enumerate(src):
        #     yield (no, line)
        yield from enumerate(src, start=1)

def gen_grep(pat, lines):
    patc = re.compile(pat)
    return ((no, line) for no, line in lines if patc.search(line))

if __name__ == '__main__':
    py_names = gen_ls('./', '*.py')
    py_files = gen_open(py_names)
    py_lines = gen_cat2(py_files)
    py_pat_lines = gen_grep('import', py_lines)

    count = 0
    for no, line in py_pat_lines:
        print('Matches:L%d: %s' % (no, line))
        count += 1

    print()
    print('Total: ', count)
