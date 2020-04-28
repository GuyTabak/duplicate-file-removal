from duplicate_file_removal.file_record import FileRecord, RecordsDictionary
from duplicate_file_removal.logger import logger

from typing import List, Tuple
from os import path


# TODO: Tests
class RecordsProcessor:
    @staticmethod
    def remove_duplicates(*priority: str, records: RecordsDictionary) -> None:
        """

        :param priority: Duplicate records from @records will be removed according to this variable, descending order.
                        Each priority path has to be absolute.
        :param records: result of the scanner module, duplicate files will be removed and saved according to the
                        @priority.
        :return:
        """

        for path_ in priority:
            if not path.isabs(path_):
                raise RuntimeError("Priority path is not absolute")
        priority = map(lambda x:  path.abspath(x), priority)  # TODO: This will probably fail

        for record in filter(lambda x: len(x) > 1, records.items()):
            RecordsProcessor.remove_duplicate_normalized(record, *priority)

    @classmethod
    def remove_duplicate_normalized(cls, records: List[FileRecord], *priority) -> None:
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
                if record.full_path.startswith(path_):
                    candidates.append((path_, record))  # Sorted by priority

        if len(candidates) == 0:  # TODO: Think this through
            record_to_keep = records[0]
        else:
            _, record_to_keep = cls.highest_specificity(candidates)

        cls.delete_records(record_to_keep, records)

    @classmethod
    def highest_specificity(cls, candidates: List[Tuple[str, FileRecord]]) -> Tuple[str, FileRecord]:
        highest_priority = candidates[0]
        for candidate in candidates[1:]:
            if candidate[0].startswith(highest_priority):
                highest_priority = candidate[0]
        return highest_priority

    @staticmethod
    def delete_records(avoid_deletion: FileRecord, records: List[FileRecord]):
        for record in filter(lambda x: x is not avoid_deletion, records):
            logger.info(f"Duplicate file was deleted: {record.full_path}")  # TODO: Move to a different log file
            record.delete_record()
