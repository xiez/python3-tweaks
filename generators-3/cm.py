import tempfile, shutil
import sys
from contextlib import contextmanager


class GeneratorCM:
    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        return next(self.gen)

    def __exit__(self, etype, val, tb):
        try:
            if etype is None:
                next(self.gen)
            else:
                self.gen.throw(etype, val, tb)
            raise RuntimeError("Generator did't stop")
        except StopIteration:
            return True
        except:
            if sys.exc_info[1] is not val:
                raise

def my_cm(func):
    def run(*args, **kwargs):
        return GeneratorCM(func(*args, **kwargs))
    return run

@contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)

@my_cm
def tempdir2():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)

if __name__ == '__main__':
    with tempdir() as dirname:
        print(dirname)

    with tempdir2() as dirname:
        print(dirname)
