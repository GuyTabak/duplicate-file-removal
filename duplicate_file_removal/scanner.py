from datetime import datetime
from os import walk, path
from re import search
from typing import List, Tuple, Optional

from duplicate_file_removal.database.db_manager import DBManager
from duplicate_file_removal.database.model_cursor import execute
from duplicate_file_removal.database.model_queries.file_record_query import save_file_record_to_db
from duplicate_file_removal.database.model_queries.scan_queries import insert_scan_start, \
    update_scan_completion_time_query
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
        """
        Provide a @root_dir from which the scan will walk to the 'walk' folder, and will return all files found which
        satisfy @regex if present, otherwise all files encountered (while skipping RESTRICTED_DIRECTORIES and
        RESTRICTED_FILE_EXT.
        :param root_dir: root_dir from which the scan begins
        :param regex: filter regex (file has to satisfy regex, or it will be ignored)
        :return: List of FileRecord for each file encountered under above restrictions
        """
        # TODO features:
        #  1. Save state (begin from stopping point).
        #  2. Add API for cloud storage
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
        """Scan and produce FileRecord for files under all paths. See 'Scanner.scan func for more info"""
        res = []
        for path_ in paths:
            res += cls.scan(path_, regex=regex)

        return res

    @classmethod
    def scan_by_file_extension(cls, extension: List[str], *paths) -> List[FileRecord]:
        """
        :param extension: Any file, who's extension is not present in this list will be ignored.
        :param paths: All paths from which to start the scan.
        :return: All records with ext in @extension under any of @paths path
        """
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
    def _is_valid_file_for_scan(cls, file_path):
        """
        Determines if a file is valid for scan:
        1. File has to exist.
        2. File can't have an any of the class's @cls.RESTRICTED_FILE_EXT extension
        3. File can't surpass max_file_size
        :param file_path:
        :return: True if valid else False
        """
        max_file_size = 10  # TODO: Move to configuration
        try:
            if path.getsize(file_path) / (1024 * 2) > max_file_size:
                return False
            _, ext = path.splitext(file_path)
            if ext in cls.RESTRICTED_FILE_EXT:
                return False
        except (PermissionError, OSError, WindowsError) as e:
            logger.info(f"Failed in file validation:\n{e}")
            return False

        return True

    @classmethod
    def save_scan_results(cls, file_records: List[FileRecord], scan_id: Optional[int] = None):
        """ Saves scan results to local db for later use, returns scan_id """
        manager = DBManager()
        connection_ = manager.connection
        if not scan_id:
            execute(connection_, insert_scan_start(), (datetime.now(),))
            scan_id = manager.last_insert_rowid()

        execute(connection_, update_scan_completion_time_query(), (datetime.now(), scan_id), commit=True)

        for file_record in file_records:
            query, params = save_file_record_to_db(file_record, scan_id)
            execute(connection_, query, params)
        connection_.commit()

        return scan_id
