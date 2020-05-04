from collections.abc import Iterable


def ignore_exceptions(func: callable, *args, **kwargs):
    # noinspection PyBroadException
    try:
        return func(args, kwargs)
    except Exception:
        pass


def count(iterable_: Iterable):
    return sum(1 for _ in iterable_)
