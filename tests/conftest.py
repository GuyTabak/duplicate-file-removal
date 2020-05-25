from os import urandom
from random import randrange
from tempfile import TemporaryDirectory, NamedTemporaryFile, TemporaryFile
from typing import Tuple
from uuid import uuid4

from pytest import fixture

from duplicate_file_removal.database.db_manager import DBManager
from duplicate_file_removal.scanner import Scanner


@fixture(scope="module")
def scanner():
    # Temporary Files\Directories are created in the 'AppData' path which is restricted in the code
    Scanner.RESTRICTED_DIRECTORIES.remove("AppData")
    yield Scanner
    Scanner.RESTRICTED_DIRECTORIES.append("AppData")


@fixture(scope="module")
def binary_data():
    return urandom(4097)


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
            with NamedTemporaryFile(dir=cur_root_dir.name, delete=False, suffix=".ext") as f:
                f.write(uuid4().bytes)
                holder.append(f)
            files_counter += 1

    yield files_counter, root_dir.name

    # Cleanup, because fixture cleanup throws exception
    for temp_ele in reversed(holder):
        if type(temp_ele) == TemporaryDirectory:
            temp_ele.cleanup()


@fixture(scope="module")
def gen_files_by_specification() -> callable:
    def inner_func(num_of_same_files: int, num_of_unique_files: int, extension='') -> TemporaryDirectory:
        const_data = uuid4().bytes
        root_dir = TemporaryDirectory()
        if extension:
            extension = '.' + extension

        # Create duplicate files
        for file in range(num_of_same_files):
            with NamedTemporaryFile(dir=root_dir.name, delete=False, suffix=extension) as f:
                f.write(const_data)
        # Create unique files
        for file in range(num_of_unique_files):
            with NamedTemporaryFile(dir=root_dir.name, delete=False, suffix=extension) as f:
                f.write(uuid4().bytes)

        return root_dir

    yield inner_func


@fixture(scope="module")
def db_path():
    f = TemporaryFile(delete=False)
    yield f.name


@fixture(scope="module")
def db_manager(db_path) -> DBManager:
    yield DBManager(db_path)
