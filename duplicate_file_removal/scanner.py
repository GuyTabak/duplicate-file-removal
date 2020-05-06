from os import walk, path
from re import search
from typing import List, Tuple

from duplicate_file_removal.file_record import FileRecord
from duplicate_file_removal.logger import logger


class Scanner:
    RESTRICTED_DIRECTORIES = ["Program Files", "Program Files (x86)", "Windows", "$Recycle.Bin", "AppData",
                              "ProgramData"]
    RESTRICTED_FILE_EXT = [".sys", ".dll", ".obj", ".py", ".go", ".html", ".js", ".s", ".md", ".ts", ".css", ".json",
                           ".pyc"]

    # TODO: handle edge cases:
    #  - permissions( Sys, other users, etc...)
    #  - different OS
    #  - network storage
    @classmethod
    def scan(cls, root_dir: str, regex: str = '') -> List[FileRecord]:
        # TODO features:
        #  1. Save state (begin from stopping point).
        #  2. Add API for cloud storage
        # 3.
        is_valid, invalid_dir_list = cls._is_valid_root_directory_for_scan(root_dir)
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
                if not cls._is_valid_file_for_scan(file_path):
                    continue
                if regex and not search(regex, file_path):  # If regex supplied, but search returns empty, skip file.
                    continue
                try:
                    res.append(FileRecord(file_path))
                except (PermissionError, OSError) as e:
                    logger.info(f"Failed to scan file:\n{e}")
        return res

    @classmethod
    def scan_multiple_paths(cls, *paths: str, regex='') -> List[FileRecord]:
        res = []
        for path_ in paths:
            res += cls.scan(path_, regex=regex)

        return res

    @classmethod
    def scan_by_file_extension(cls, extension: List[str], *paths) -> List[FileRecord]:
        regex_str = ""
        extension = map(lambda x: x[1:] if x.startswith('.') else x, extension)  # To accept both '.ext' and 'ext'
        extension_template = '\\.{file_ext}+$'

        for ext in extension:
            regex_str += extension_template.format(file_ext=ext) + '|'
        regex_str = regex_str[:-1]  # remove last '|'
        return cls.scan_multiple_paths(*paths, regex=regex_str)

    @classmethod
    def _is_valid_root_directory_for_scan(cls, dir_: str) -> Tuple[bool, List[str]]:
        """
        :param dir_: dir path
        :return: (True, []) if valid for scan, else (False, [List of bad component in dir_])
        """
        path_elements = map(str, path.normpath(dir_).split(path.sep))
        invalids_dirs = []
        for dir_ in filter(lambda x: x in cls.RESTRICTED_DIRECTORIES, path_elements):
            invalids_dirs.append(dir_)

        return (True, []) if not invalids_dirs else (False, invalids_dirs)

    @classmethod
    def _is_valid_file_for_scan(cls, file_path, max_file_size: float = 10):
        """
        Determines if a file is valid for scan:
        1. File has to exist.
        2. File can't have an any of the class's @cls.RESTRICTED_FILE_EXT extension
        3. File can't surpass max_file_size
        :param file_path:
        :param max_file_size: max size of file allowed, in mega bytes.
        :return: True if valid else False
        """
        try:
            # TODO: Remove when NTFS scan is added
            if path.getsize(file_path) / (1024 * 2) > max_file_size:
                return False
            _, ext = path.splitext(file_path)
            if ext in cls.RESTRICTED_FILE_EXT:
                return False
        except (PermissionError, OSError, WindowsError) as e:
            logger.info(f"Failed in file validation:\n{e}")
            return False

        return True
