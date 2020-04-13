from duplicate_file_removal.file_record import Record, RecordsDictionary
from os import walk, path


class Scanner:
    RESTRICTED_DIRECTORIES = ["Program Files", "Program Files (x86)", "Windows"]

    # TODO: TEST, heavily.
    @staticmethod
    def scan_and_generate_records(base_directory: str, record_dict: RecordsDictionary = None) -> RecordsDictionary:
        # TODO: handle edge cases:
        #  - permissions( Sys, other users, etc...)
        #  - different OS
        #  - network storage

        if not record_dict:
            record_dict = RecordsDictionary()

        # If we are already in a restricted path, return without scan
        path_elements = path.normpath(base_directory).split(path.sep)
        if list(filter(lambda ele: ele in Scanner.RESTRICTED_DIRECTORIES, iter(path_elements))):
            return record_dict

        for root, dirs, files in walk(base_directory):
            # TODO: Test which is faster
            # dirs = list(filter(lambda x: x not in Scanner.RESTRICTED_DIRECTORIES, dirs))

            # avoid restricted directories
            for index, dir_ in enumerate(dirs):
                if dir_ in Scanner.RESTRICTED_DIRECTORIES:
                    del dirs[index]

            for file_ in files:
                r = Record(path.join(root, file_))
                record_dict.add(r)

        return record_dict
