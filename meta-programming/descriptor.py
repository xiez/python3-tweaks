from functools import wraps, partial
import os


def debug(func):
    """
    g = debug(f)
    g(1,2) = debug(f(1,2))
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if callable(func):
            print('DEBUG: ' + func.__qualname__)
            return func(*args, **kwargs)
        elif isinstance(func, staticmethod) or isinstance(func, classmethod):
            print('DEBUG: ' + func.__func__.__qualname__)
            print(args)
            print(kwargs)
            return func.__func__(*args, **kwargs)

    return wrapper

def debugargs(prefix='***'):
    """
    debug = debugargs(prefix='')
    g = debug(f)
    g(1,2) = debug(f(1,2)) = debugargs(prefix='')(f(1,2))
    """
    def debug(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(prefix + ': ' + func.__qualname__)
            return func(*args, **kwargs)
        return wrapper
    return debug

def debughack(func=None, prefix='***'):
    if func is None:
        return partial(debughack, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(prefix + ': ' + func.__qualname__)
        return func(*args, **kwargs)
    return wrapper


# @debug
# @debugargs()
@debughack(prefix='---')
def add(a1, a2):
    return a1 + a2

# class decorator ##############################
def debugmethods(cls):
    """
    g = debugmethods(cls)
    g().add = debugmethods(cls()).add
    """

    for k, func in vars(cls).items():
        if callable(func) or isinstance(func, staticmethod) or isinstance(func, classmethod):
            setattr(cls, k, debug(func))

    return cls


@debugmethods
class Spam(object):
    def add(self, a1, a2):
        return a1 + a2

    @staticmethod
    def s_add(a1, a2):
        return a1 + a2

    @classmethod
    def c_add(cls, a1, a2):
        print(cls)
        return a1 + a2

# debug access ########################################
def debugattrs(cls):
    orig_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print('Get: ', name)
        return orig_getattribute(self, name)

    cls.__getattribute__ = __getattribute__
    return cls

@debugattrs
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# metaclass ########################################
class debugmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        clsobj = debugmethods(clsobj)
        return clsobj

class Base(metaclass=debugmeta):
    pass

class A(Base):
    def a(self):
        print('a')

class B(Base):
    def b(self):
        print('b')

class AB(A, B):
    def ab(self):
        super().a()
        super().b()

# signature 39:24 ########################################
from inspect import Parameter, Signature
def make_signature(names):
    return Signature(
        [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    )

class StructMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj._fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj

class Structure(metaclass=StructMeta):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)

    def __repr__(self):
        args = ', '.join(repr(getattr(self, name)) for name in self._fields)
        return type(self).__name__ + '(' + args + ')'


# class Structure:
#     __signature__ = make_signature([])
#     def __init__(self, *args, **kwargs):
#         bound = self.__signature__.bind(*args, **kwargs)
#         for name, val in bound.arguments.items():
#             setattr(self, name, val)

class Descriptor:
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, cls):
        print('get')
        print(cls)

        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError('Expected %s' % self.ty)
        super().__set__(instance, value)

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str

class Positive(Typed):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >=0')
        super().__set__(instance, value)

class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError('Too big')
        super().__set__(instance, value)

import re
class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError('Invalid string')
        super().__set__(instance, value)

class PositiveInteger(Integer, Positive): pass

class SizedString(String, Sized): pass

class SizedRegexString(String, Sized, Regex): pass


class Stock(Structure):
    _fields = ['name', 'shares', 'price']

    name = SizedRegexString('name', maxlen=4, pat='[A-Z]+$')
    shares = PositiveInteger('shares')
    price = Float('price')

    # @property
    # def shares(self):
    #     return self._shares

    # @shares.setter
    # def shares(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('expected int')
    #     if value < 0:
    #         raise ValueError('Must be >= 0')
    #     self._shares = value


def add_signature(*names):
    def decorate(cls):
        cls.__signature__ = make_signature(names)
        return cls
    return decorate

@add_signature('x', 'y')
class Point(Structure):
    pass

class Host(Structure):
    _fields = ['hostname', 'port']
