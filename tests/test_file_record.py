from duplicate_file_removal.file_record import FileRecord, RecordsDictionary

from pytest import fixture

from tempfile import TemporaryDirectory
from os import path
from hashlib import md5
from uuid import uuid4


@fixture(scope="module")
def temp_file_path(binary_data):
    temp_dir = TemporaryDirectory('w+')
    file_name = uuid4().hex + '.end'

    file_ = open(path.join(temp_dir.name, file_name), 'wb')
    file_.write(binary_data)
    file_.close()

    yield file_.name  # So that temp_dir won't be deleted until end of module execution


@fixture(scope="module")
def record(temp_file_path):
    return FileRecord(temp_file_path)


def test_record_hash(record, binary_data):
    assert record.hash == md5(binary_data).hexdigest()


def test_dup_record_in_record_dictionary(record):
    d = RecordsDictionary()
    d.add(record)
    d.add(record)

    assert len(d) == 1
    assert len(d[record.hash]) == 2
