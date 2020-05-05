from os import path
from tempfile import TemporaryDirectory

from pytest import raises, mark

from duplicate_file_removal.file_record import RecordStatus
from duplicate_file_removal.processor import RecordsProcessor
from tests.utils.util import ignore_exceptions, count, no_stdout


def test_remove_duplicates():
    with raises(RuntimeError):  # make sure paths provided have to be absolute
        RecordsProcessor.remove_duplicates([], "..\\SomeFolder")


def test_scanner_results_to_groups(scanner, gen_files_by_specification):
    num_of_dup_files = 10
    num_of_unique_files = 5

    base_dir = gen_files_by_specification(num_of_dup_files, num_of_unique_files)
    res = scanner.scan(base_dir.name)
    res = RecordsProcessor.scanner_results_to_groups(res)
    assert len(res) == 1  # occurrences for unique files filtered, and 1 occurrence for the 10 duplicate files

    dup_files_list = next(iter(res.values()))  # get the value of the first element
    assert len(dup_files_list) == num_of_dup_files


def test_remove_duplicate_normalized(binary_data, scanner):
    """
    Test to insure that given a more specific priority in a less specificity,
    then specificity > priority
    """
    temp_dir_1 = TemporaryDirectory()
    temp_file_name_1 = path.join(temp_dir_1.name, "file_1")
    with open(temp_file_name_1, "wb") as f:
        f.write(binary_data)

    temp_dir_2 = TemporaryDirectory(dir=temp_dir_1.name)
    temp_file_name_2 = path.join(temp_dir_2.name, "file_2")
    with open(temp_file_name_2, "wb") as f:
        f.write(binary_data)

    records = scanner.scan(temp_dir_1.name)
    assert len(records) == 2  # sanity check
    priority = ["C:\\", temp_dir_2.name]

    RecordsProcessor._remove_duplicate_normalized(records, *priority)

    assert records[0].status == RecordStatus.deleted
    assert records[1].status == RecordStatus.exists

    # TemporaryDirectory cleanup warning ignored
    ignore_exceptions(temp_dir_1.cleanup)
    ignore_exceptions(temp_dir_2.cleanup)


# noinspection PyTypeChecker
def test_highest_specificity():
    chosen_one = object()

    candidates = [("C:\\", object()), ("C:\\specific", object()), ("C:\\specific\\choose_me", chosen_one)]
    assert chosen_one is RecordsProcessor._highest_specificity(candidates)


@mark.parametrize("is_simulation,expected", [(False, 2), (True, 3)])
def test_delete_records(is_simulation, expected, scanner, gen_files_by_specification):
    # If changed, adjust parametrize value accordingly
    num_of_dup_files = 2
    num_of_unique_files = 5

    base_dir = gen_files_by_specification(num_of_dup_files, num_of_unique_files)
    res = RecordsProcessor.scanner_results_to_groups(scanner.scan(base_dir.name))
    duplicate_records = next(iter(res.values()))

    res.add(duplicate_records[0])  # Try to 'cheat' the scanner and have two FileRecords to the same physical file
    with no_stdout():
        RecordsProcessor.delete_records(duplicate_records[0], duplicate_records, is_simulation)

    assert count(filter(lambda x: x.status == RecordStatus.exists, duplicate_records)) == expected
