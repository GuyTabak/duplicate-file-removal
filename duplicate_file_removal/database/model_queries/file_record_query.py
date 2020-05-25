from typing import Tuple

from duplicate_file_removal.database.models.file_record_model import FileRecordModel
from duplicate_file_removal.file_record import FileRecord


# noinspection PyProtectedMember
def save_file_record_to_db(file_record: FileRecord, scan_id: int) -> Tuple[str, Tuple]:
    query = f"INSERT INTO {FileRecordModel.table_name()} (ext, file_path, hash_value, size, scan_id)" \
            f"VALUES(?,?,?,?,?)"
    return query, (file_record.ext, file_record.file_path, file_record._hash_cache, file_record.size, scan_id)
