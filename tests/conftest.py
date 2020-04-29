from duplicate_file_removal.scanner import Scanner

from os import urandom

from pytest import fixture


@fixture(scope="module")
def scanner():
    # Temporary Files\Directories are created in the 'AppData' path which is restricted in the code
    Scanner.RESTRICTED_DIRECTORIES.remove("AppData")
    yield Scanner
    Scanner.RESTRICTED_DIRECTORIES.append("AppData")


@fixture(scope="module")
def binary_data():
    return urandom(4097)


def ignore_exceptions(func: callable):
    # noinspection PyBroadException
    try:
        func()
    except Exception:
        pass
