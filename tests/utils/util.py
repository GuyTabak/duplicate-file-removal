import sys
from collections.abc import Iterable
from contextlib import contextmanager
from os import path


def ignore_exceptions(func: callable, *args, **kwargs):
    # noinspection PyBroadException
    try:
        if args and kwargs:
            return func(*args, *kwargs)
        elif args and not kwargs:
            return func(*args)
        elif not args and kwargs:
            return func(*kwargs)
        else:
            return func()
    except Exception:
        pass


def count(iterable_: Iterable):
    return sum(1 for _ in iterable_)


@contextmanager
def no_stdout():
    save_stdout = sys.stdout
    from tempfile import TemporaryDirectory
    temp = TemporaryDirectory()
    sys.stdout = open(path.join(temp.name, 'file'), "w")
    yield
    sys.stdout = save_stdout
