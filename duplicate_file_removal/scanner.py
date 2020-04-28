from duplicate_file_removal.file_record import FileRecord, RecordsDictionary
from duplicate_file_removal.logger import logger

from os import walk, path


class Scanner:
    RESTRICTED_DIRECTORIES = ["Program Files", "Program Files (x86)", "Windows", "$Recycle.Bin", "AppData",
                              "ProgramData"]
    RESTRICTED_FILE_EXT = [".sys"]

    @classmethod
    def scan_and_generate_records(cls, root_directory: str, records: RecordsDictionary = None) -> RecordsDictionary:
        # TODO: handle edge cases:
        #  - permissions( Sys, other users, etc...)
        #  - different OS
        #  - network storage

        if not records:
            records = RecordsDictionary()

        if not cls.is_valid_root_directory(root_directory):
            return records

        for root, dirs, files in walk(root_directory):
            for index, dir_ in enumerate(dirs):  # avoid restricted directories
                if dir_ in cls.RESTRICTED_DIRECTORIES:
                    del dirs[index]

            for file_ in files:
                file_path = path.join(root, file_)
                if not cls.is_valid_file(file_path):
                    continue
                try:
                    r = FileRecord(file_path)
                    records.add(r)
                except (PermissionError, OSError) as e:
                    logger.info(f"Failed to scan file:\n{e}")
        return records

    @classmethod
    def scan_multiple_paths(cls, *paths: str, records: RecordsDictionary = None) -> RecordsDictionary:
        if not records:
            records = RecordsDictionary()

        for path_ in paths:
            cls.scan_and_generate_records(path_, records)

        return records

    @classmethod
    def is_valid_root_directory(cls, dir_):
        path_elements = path.normpath(dir_).split(path.sep)
        if list(filter(lambda ele: ele in Scanner.RESTRICTED_DIRECTORIES, iter(path_elements))):
            return False
        return True

    @classmethod
    def is_valid_file(cls, file_path):
        try:
            # TODO: Remove when NTFS scan is added
            if path.getsize(file_path) / (1024 * 2) > 10:  # Ignore files larger than 10mb
                return False
            _, ext = path.splitext(file_path)
            if ext in cls.RESTRICTED_FILE_EXT:
                return False
        except (PermissionError, OSError, WindowsError) as e:
            logger.info(f"Failed in file validation:\n{e}")
            return False

        return True
