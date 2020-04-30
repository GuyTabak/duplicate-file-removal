from duplicate_file_removal.file_record import FileRecord, RecordsDictionary
from duplicate_file_removal.logger import res_logger

from typing import List, Tuple
from os import path


class RecordsProcessor:
    @staticmethod
    def remove_duplicates(records: RecordsDictionary, *priority: str) -> None:
        """

        :param priority: Duplicate records from @records will be removed according to this variable, descending order.
                        Each priority path has to be absolute.
        :param records: result of the scanner module, duplicate files will be removed and saved according to the
                        @priority.
        :return:
        """
        priority = map(lambda x: path.normpath(x), priority)
        for path_ in priority:
            if not path.isabs(path_):
                raise RuntimeError(f"Priority path is not absolute: {path_}")

        for file_records in records.values():
            RecordsProcessor._remove_duplicate_normalized(file_records, *priority)

    @classmethod
    def _remove_duplicate_normalized(cls, records: List[FileRecord], *priority) -> None:
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
        cls.delete_records(record_to_keep, records)

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
    def delete_records(cls, avoid_deletion: FileRecord, records: List[FileRecord]):
        for record in filter(lambda x: x is not avoid_deletion, records):
            res_logger.info(f"Duplicate file was deleted: {record.file_path}")
            record.delete_record()
