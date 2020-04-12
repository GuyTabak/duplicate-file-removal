from typing import Dict, List
from hashlib import md5
from os import path


class Record:
    def __init__(self, full_path: str):
        if not path.isfile(full_path):
            raise RuntimeError(f"Path provided: '{full_path}' is not valid.")
        full_name = path.basename(full_path)
        self.name, self.ext = path.splitext(full_name)
        self.dir, _ = path.splitext(full_path)
        self.full_path: str = full_path
        self.hash_ = self.md5_file(full_path)

    @staticmethod
    def md5_file(file_name):
        hash_md5 = md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


class RecordsDictionary:
    def __init__(self):
        self.dict_: Dict[str, List[Record]] = dict()

    def add(self, record: Record):
        recorded_files = self.dict_.get(record.hash_, [])
        recorded_files.append(record)
