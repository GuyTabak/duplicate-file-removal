from duplicate_file_removal.file_record import FileRecord, RecordsDictionary

from os import walk, path


class Scanner:  # TODO: consider utility module, and class not needed
    # TODO: move the config file
    RESTRICTED_DIRECTORIES = ["Program Files", "Program Files (x86)", "Windows", "$Recycle.Bin", "AppData"]
    RESTRICTED_FILE_EXT = ["sys"]

    # TODO: TEST, heavily.
    # TODO: split to filter functions
    @classmethod
    def scan_and_generate_records(cls, root_directory: str, records_dict: RecordsDictionary = None) \
            -> RecordsDictionary:
        # TODO: handle edge cases:
        #  - permissions( Sys, other users, etc...)
        #  - different OS
        #  - network storage

        if not records_dict:
            records_dict = RecordsDictionary()

        if not cls.is_valid_root_directory(root_directory):
            return records_dict

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
                    records_dict.add(r)
                except PermissionError or OSError:
                    continue  # TODO: log
        return records_dict

    @classmethod
    def is_valid_root_directory(cls, dir_):
        path_elements = path.normpath(dir_).split(path.sep)
        if list(filter(lambda ele: ele in Scanner.RESTRICTED_DIRECTORIES, iter(path_elements))):
            return False
        return True

    @classmethod
    def is_valid_file(cls, file_path):
        try:
            if path.getsize(file_path) / (1024 * 2) > 10:  # Ignore files larger than 10mb
                return False
            if path.basename(file_path) in cls.RESTRICTED_FILE_EXT:
                return False
        except (PermissionError, OSError, WindowsError):
            # TODO: Log
            return False

        return True
