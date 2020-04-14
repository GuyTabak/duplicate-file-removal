from duplicate_file_removal.scanner import Scanner

from tempfile import TemporaryDirectory, NamedTemporaryFile
from random import randrange
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


def test_scan_and_generate_records_1(random_dir_and_files):
    num_of_files, dir_ = random_dir_and_files
    records_dict = Scanner.scan_and_generate_records(dir_)

    assert len(records_dict) == num_of_files
