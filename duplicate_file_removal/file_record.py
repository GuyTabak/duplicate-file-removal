from enum import Enum
from hashlib import md5
from logging import Logger
from os import path, remove, stat
from typing import Optional


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
        self._hash_cache: Optional[str] = None
        self.size: int = stat(self.file_path).st_size  # size in bytes  # TODO: check performance

    @property
    def hash(self):
        if self._hash_cache:
            return self._hash_cache
        self._hash_cache = self.md5_file(self.file_path)
        return self._hash_cache

    def delete_record(self, logger: Optional[Logger]):
        self.status = RecordStatus.deleted
        remove(self.file_path)
        if logger:
            logger.info(f"File deleted: {self.file_path.encode('utf-8')}")

    @staticmethod
    def md5_file(file_name):
        hash_md5 = md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()


class RecordsDictionary(dict):
    def __init__(self, hash_by="hash"):
        super(RecordsDictionary, self).__init__()
        self.attr = hash_by

    def add(self, record: FileRecord):
        self.setdefault(getattr(record, self.attr), []).append(record)
