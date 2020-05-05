from os import path
from typing import List, Tuple

from duplicate_file_removal.file_record import FileRecord, RecordsDictionary
from duplicate_file_removal.logger import res_logger


class RecordsProcessor:
    @classmethod
    def remove_duplicates(cls, records: List[FileRecord], *priority: str, simulation=False) -> None:
        """
        :param records: result of the scanner module, duplicate files will be removed and saved according to the
            @priority.
        :param priority: Duplicate FileRecord(@records) will be removed according to this variable, descending order.
            Each priority path has to be absolute.
        :param simulation: If true, instead of deletion, prints to stdout the files which will be deleted and readable
            manner.
        :return:
        """
        priority = map(lambda x: path.normpath(x), priority)
        bad_paths = [path_ for path_ in filter(lambda x: not path.isabs(x), priority)]
        if bad_paths:
            raise RuntimeError(f"Following paths are not absolute: {bad_paths}")

        for _, val in cls.scanner_results_to_groups(records).items():
            RecordsProcessor._remove_duplicate_normalized(val, *priority, simulation)

    @classmethod
    def scanner_results_to_groups(cls, records: List[FileRecord]) -> RecordsDictionary:
        records_by_size = cls.group_by_size(records)
        cls.remove_unique(records_by_size)  # unique by size

        records_by_hash = cls.records_by_size_to_by_hash(records_by_size)
        cls.remove_unique(records_by_hash)  # unique by hash

        return records_by_hash

    @classmethod
    def group_by_size(cls, records: List[FileRecord]) -> RecordsDictionary:
        res = RecordsDictionary(hash_by="size")
        for record in records:
            res.add(record)
        return res

    @classmethod
    def remove_unique(cls, records: RecordsDictionary) -> None:
        for key in list(records.keys()):  # creating list is required for deletion during iteration
            if len(records[key]) == 1:
                records.pop(key)

    @classmethod
    def records_by_size_to_by_hash(cls, records: RecordsDictionary):
        res = RecordsDictionary()
        for val in records.values():
            for record in val:
                res.add(record)
        return res

    @classmethod
    def _remove_duplicate_normalized(cls, records: List[FileRecord], *priority, simulation=False) -> None:
        """
        This function is doing some smart decisions of which duplicate to delete:
        If priority_path_a is included in priority_path_b, but priority_path_b is ranked higher,
        the record under priority_path_b will be deleted (we choose specificity over priority).
        :param records:
        :param priority:
        :return:
        """
        candidates: List[Tuple[str, FileRecord]] = []

        for path_ in priority:
            for record in records:
                if record.file_path.startswith(path_):
                    candidates.append((path_, record))  # Sorted by priority

        if len(candidates) == 0:  # TODO: Think this through
            record_to_keep = records[0]
        else:
            record_to_keep = cls._highest_specificity(candidates)

        # TODO: add verification that 'record_to_keep' is not corrupted
        cls.delete_records(record_to_keep, records, simulation)

    @classmethod
    def _highest_specificity(cls, candidates_desc: List[Tuple[str, FileRecord]]) -> FileRecord:
        """
        See 'remove_duplicate_normalized' for reasoning.
        :param candidates_desc: List of candidates(to avoid deletion), in descending priority
        :return: The FileRecord with highest specificity
        """
        priority_path_index = 0
        record_index = 1

        highest_priority = candidates_desc[0]  # First element has highest priority
        for candidate in candidates_desc[1:]:
            if candidate[priority_path_index].startswith(highest_priority[priority_path_index]):
                highest_priority = candidate
        return highest_priority[record_index]

    @classmethod
    def delete_records(cls, avoid_deletion: FileRecord, records: List[FileRecord], simulation=False):
        if simulation:
            print(f"Files bellow are duplicate of '{avoid_deletion.file_path}':")
        for record in filter(lambda x: x.file_path is not avoid_deletion.file_path, records):
            res_logger.info(f"Duplicate file was deleted: {record.file_path}")
            if not simulation:
                record.delete_record(res_logger)
            else:
                print(f"File {record.file_path} would have been deleted.")
