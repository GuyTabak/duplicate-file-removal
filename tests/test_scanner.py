from os import mkdir, path
from random import choice
from tempfile import NamedTemporaryFile

from pytest import fixture

from duplicate_file_removal.scanner import Scanner


@fixture(scope='module')
def restricted_dir_and_files(random_dir_and_files, scanner):
    # Generate a temp dir with one restricted file and one restricted folder
    _, dir_ = random_dir_and_files
    open(path.join(dir_, "file_name" + choice(Scanner.RESTRICTED_FILE_EXT)), "w")
    temp_dir_path = path.join(dir_, choice(scanner.RESTRICTED_DIRECTORIES))
    mkdir(temp_dir_path)
    NamedTemporaryFile(dir=temp_dir_path, delete=False)

    yield random_dir_and_files  # The new folder and files are contained in the provided fixture


def test_scan(scanner, random_dir_and_files):
    num_of_files, dir_ = random_dir_and_files
    res = Scanner.scan(dir_)
    assert len(res) == num_of_files


def test_restricted_scan(restricted_dir_and_files):
    # Make sure that even if root directory of the scan is valid, it doesn't scan or access a
    # restricted folder or file
    num_of_files, dir_ = restricted_dir_and_files
    res = Scanner.scan(dir_)

    assert len(res) == num_of_files


def test_scan_multiple_paths(random_dir_and_files, scanner):
    num_of_files, dir_ = random_dir_and_files
    assert num_of_files * 2 == len(scanner.scan_multiple_paths(dir_, dir_))
