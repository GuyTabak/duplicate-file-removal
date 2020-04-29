from duplicate_file_removal.file_record import RecordsDictionary, RecordStatus
from duplicate_file_removal.processor import RecordsProcessor

from tempfile import TemporaryDirectory
from pytest import raises
from os import path

from tests.conftest import ignore_exceptions


def test_remove_duplicates():
    with raises(RuntimeError):
        RecordsProcessor.remove_duplicates(RecordsDictionary(), "..\\SomeFolder")


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

    records = scanner.scan_and_generate_records(temp_dir_1.name)
    dup_list = list(records.values())[0]
    assert len(dup_list) == 2  # sanity check
    priority = ["C:\\", temp_dir_2.name]

    RecordsProcessor._remove_duplicate_normalized(dup_list, *priority)

    assert dup_list[0].status == RecordStatus.deleted
    assert dup_list[1].status == RecordStatus.exists

    # TemporaryDirectory cleanup warning ignored
    ignore_exceptions(temp_dir_1.cleanup)
    ignore_exceptions(temp_dir_2.cleanup)


# noinspection PyTypeChecker
def test_highest_specificity():
    chosen_one = object()

    candidates = [("C:\\", object()), ("C:\\specific", object()), ("C:\\specific\\choose_me", chosen_one)]
    assert chosen_one is RecordsProcessor._highest_specificity(candidates)
