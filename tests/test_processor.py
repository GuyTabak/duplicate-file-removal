from duplicate_file_removal.processor import RecordsProcessor
from duplicate_file_removal.file_record import RecordsDictionary
from pytest import raises

def test_remove_duplicates():
    with raises(RuntimeError):
        RecordsProcessor.remove_duplicates(RecordsDictionary(), "..\\SomeFolder" )


def test_remove_duplicate_normalized(scanner):
    pass


# noinspection PyTypeChecker
def test_highest_specificity():
    candidates = [("C:\\", None), ("C:\\specific", None), ("C:\\specific\\choose_me", None)]
    chosen_one = RecordsProcessor._highest_specificity(candidates)
    assert chosen_one == "C:\\specific\\choose_me"


def test_delete_records():
    pass
