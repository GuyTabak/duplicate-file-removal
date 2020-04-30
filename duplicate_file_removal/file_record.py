from os import path, remove
from hashlib import md5
from enum import Enum


class RecordStatus(Enum):
    deleted, exists= range(2)


class FileRecord:
    def __init__(self, full_path: str, create_hash: bool=False, file_size: int = None):
        full_path = path.normpath(full_path)
        if not path.isfile(full_path):
            raise RuntimeError(f"Path provided: '{full_path}' is not valid.")

        self.status = RecordStatus.exists
        file_name = path.basename(full_path)

        _, self.ext = path.splitext(file_name)
        self.full_path = full_path
        self.hash_cash = None
        if create_hash:
            self.hash_cash = self.md5_file(full_path)
        self.file_size = file_size

    @property
    def hash_(self):
        if self.hash_cash:
            return self.hash_cash
        self.hash_cash = self.md5_file(self.full_path)
        return self.hash_cash

    def delete_record(self):
        self.status = RecordStatus.deleted
        remove(self.full_path)

    @staticmethod
    def md5_file(file_name):
        hash_md5 = md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()


class RecordsDictionary(dict):
    def add(self, record: FileRecord):
        self.setdefault(record.hash_, []).append(record)
