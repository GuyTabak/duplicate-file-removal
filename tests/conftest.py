from duplicate_file_removal.scanner import Scanner

from tempfile import TemporaryDirectory, NamedTemporaryFile
from random import randrange
from typing import Tuple
from os import urandom
from uuid import uuid4

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


def ignore_exceptions(func: callable, *args, **kwargs):
    # noinspection PyBroadException
    try:
        return func(args, kwargs)
    except Exception:
        pass


@fixture(scope="module")
def random_dir_and_files() -> Tuple[int, str]:
    files_counter = 0
    root_dir = TemporaryDirectory()

    holder = []  # Just so that temp dirs and files won't be deleted immediately
    cur_root_dir = root_dir
    for _ in range(randrange(1, 5)):
        cur_root_dir = TemporaryDirectory(dir=cur_root_dir.name)
        holder.append(cur_root_dir)
        for i in range(randrange(1, 5)):
            with NamedTemporaryFile(dir=cur_root_dir.name, delete=False) as f:
                f.write(uuid4().bytes)
                holder.append(f)
            files_counter += 1

    yield files_counter, root_dir.name

    # Cleanup, because fixture cleanup throws exception
    for temp_ele in reversed(holder):
        if type(temp_ele) == TemporaryDirectory:
            temp_ele.cleanup()
