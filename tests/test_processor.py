from duplicate_file_removal.processor import RecordsProcessor
from duplicate_file_removal.file_record import RecordStatus

from tempfile import TemporaryDirectory
from pytest import raises
from os import path

from tests.utils.util import ignore_exceptions, count


def test_remove_duplicates():
    with raises(RuntimeError):  # make sure paths provided have to be absolute
        RecordsProcessor.remove_duplicates([], "..\\SomeFolder")


def test_scanner_results_to_groups(scanner, gen_files_by_specification):
    num_of_dup_files = 10
    num_of_unique_files = 5

    base_dir = gen_files_by_specification(num_of_dup_files, num_of_unique_files)
    res = scanner.scan(base_dir.name)
    res = RecordsProcessor.scanner_results_to_groups(res)
    assert len(res) == 6  # 5 occurrences for unique files, and 1 occurrence for the 10 duplicate files
    assert count(filter(lambda elem: len(elem[1]) == num_of_dup_files, res.items())) == 1
    assert count((filter(lambda elem: len(elem[1]) == 1, res.items()))) == num_of_unique_files


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
