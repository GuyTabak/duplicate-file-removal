from duplicate_file_removal.scanner import Scanner

from tempfile import TemporaryDirectory, NamedTemporaryFile
from random import randrange, choice
from os import mkdir, path
from typing import Tuple
from uuid import uuid4

from pytest import fixture


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


def test_scan_and_generate_records_1(random_dir_and_files, scanner):
    num_of_files, dir_ = random_dir_and_files
    records_dict = scanner.scan_and_generate_records(dir_)

    assert len(records_dict) == num_of_files


@fixture(scope='module')
def restricted_dir_and_files(random_dir_and_files, scanner):
    _, dir_ = random_dir_and_files

    temp_dir_path = path.join(dir_, choice(scanner.RESTRICTED_DIRECTORIES))
    mkdir(temp_dir_path)
    NamedTemporaryFile(dir=temp_dir_path, delete=False)

    yield random_dir_and_files


def test_restricted_dir(restricted_dir_and_files):
    num_of_files, dir_ = restricted_dir_and_files
    records_dict = Scanner.scan_and_generate_records(dir_)

    assert len(records_dict) == num_of_files
