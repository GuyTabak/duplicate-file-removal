from os import path, remove, stat
from hashlib import md5
from enum import Enum
from typing import Union


class RecordStatus(Enum):
    deleted, exists = range(2)


class FileRecord:
    def __init__(self, path_: str):
        path_ = path.normpath(path_)
        if not path.isfile(path_):
            raise RuntimeError(f"Path provided: '{path_}' is not valid.")

        self.status = RecordStatus.exists
        _, self.ext = path.splitext(path_)
        self.file_path: str = path_
        self._hash_cash: Union[str, None] = None
        self.file_size: int = stat(self.file_path).st_size  # size in bytes

    @property
    def hash(self):
        if self._hash_cash:
            return self._hash_cash
        self._hash_cash = self.md5_file(self.file_path)
        return self._hash_cash

    def delete_record(self):
        self.status = RecordStatus.deleted
        remove(self.file_path)

    @staticmethod
    def md5_file(file_name):
        hash_md5 = md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()


class RecordsDictionary(dict):
    def add(self, record: FileRecord):
        self.setdefault(record.hash, []).append(record)
