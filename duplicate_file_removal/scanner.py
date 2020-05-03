from duplicate_file_removal.file_record import FileRecord
from duplicate_file_removal.logger import logger

from os import walk, path
from typing import List, Tuple


class Scanner:
    RESTRICTED_DIRECTORIES = ["Program Files", "Program Files (x86)", "Windows", "$Recycle.Bin", "AppData",
                              "ProgramData"]
    RESTRICTED_FILE_EXT = [".sys", ".dll", ".obj"]

    # TODO: handle edge cases:
    #  - permissions( Sys, other users, etc...)
    #  - different OS
    #  - network storage
    @classmethod
    def scan(cls, root_dir: str) -> List[FileRecord]:
        # TODO features:
        #  1. Save state (begin from stopping point).
        #  2. Add API for cloud storage
        # 3.
        is_valid, invalid_dir_list = cls.is_valid_root_directory(root_dir)
        if not is_valid:
            raise RuntimeError(f"Invalid root directory. Check that the path doesnt contain any of the following:\n"
                               f"{', '.join(invalid_dir_list)}")
        res = []
        for root, dirs, files in walk(root_dir):
            for index, dir_ in enumerate(dirs):  # avoid restricted directories
                if dir_ in cls.RESTRICTED_DIRECTORIES:
                    del dirs[index]

            for file_ in files:
                file_path = path.join(root, file_)
                if not cls.is_valid_file(file_path):
                    continue
                try:
                    res.append(FileRecord(file_path))
                except (PermissionError, OSError) as e:
                    logger.info(f"Failed to scan file:\n{e}")
        return res

    @classmethod
    def is_valid_root_directory(cls, dir_) -> Tuple[bool, List[str]]:
        path_elements = map(str, path.normpath(dir_).split(path.sep))
        invalids_dirs = []
        for dir_ in filter(lambda x: x in cls.RESTRICTED_DIRECTORIES, path_elements):
            invalids_dirs.append(dir_)

        return (True, []) if not invalids_dirs else (False, invalids_dirs)

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

# except (PermissionError, OSError) as e:
#
#
#     @classmethod
#     def scan_multiple_paths(cls, *paths: str, records: RecordsDictionary = None) -> RecordsDictionary:
#         if not records:
#             records = RecordsDictionary()
#
#         for path_ in paths:
#             cls.scan_and_generate_records(path_, records)
#
#         return records
