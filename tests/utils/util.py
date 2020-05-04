from collections.abc import Iterable


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
