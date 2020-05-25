from duplicate_file_removal.database.db_manager import DBManager
from duplicate_file_removal.database.model_cursor import execute
from duplicate_file_removal.database.models.file_record_model import FileRecordModel
from os import mkdir, path
from random import choice
from tempfile import NamedTemporaryFile

from pytest import fixture

from duplicate_file_removal.database.models.scan_model import ScanModel
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


def test_save_scan_results(scanner, random_dir_and_files, db_manager):
    num_of_files, dir_ = random_dir_and_files
    res = Scanner.scan(dir_)

    # Hack to work on the same db path
    old_path = DBManager._DEFAULT_DB_PATH
    DBManager._DEFAULT_DB_PATH = db_manager.db_path

    # init tables
    db_manager.create_table(FileRecordModel)
    db_manager.create_table(ScanModel)

    scan_id = scanner.save_scan_results(res)
    query = f"SELECT * FROM {FileRecordModel.table_name()} WHERE file_path=? and scan_id=?"
    DBManager._DEFAULT_DB_PATH = old_path  # Restore previous db path

    assert execute(db_manager.connection, query, (res[0].file_path, scan_id)).fetchone() is not None


def test_scan_by_file_extension(gen_files_by_specification, scanner):
    num_of_same_files, num_of_unique_files, ext = 5, 5, 'unique'
    root_dir_1 = gen_files_by_specification(num_of_same_files, num_of_unique_files, ext)
    root_dir_2 = gen_files_by_specification(num_of_same_files, num_of_unique_files, ext + '2')
    assert len(scanner.scan_by_file_extension([ext], root_dir_1.name, root_dir_2.name)) == 10
    assert len(scanner.scan_by_file_extension([ext, ext + '2'], root_dir_1.name, root_dir_2.name)) == 20


