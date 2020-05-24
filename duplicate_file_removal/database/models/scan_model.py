from enum import Enum

from duplicate_file_removal.database.models.base_model import BaseModel
from duplicate_file_removal.database.types import SQLiteTypes


class ScanStatus(Enum):
    initiated, completed = range(2)


class ScanModel(BaseModel):
    columns = (
        ('id', SQLiteTypes.INTEGER),
        ('scan_start_time', "timestamp"),
        ('scan_complete_time', "timestamp"),
        ('scan_status', "timestamp")
    )
    primary_keys = ('id',)

    # # TODO: test
    # @classmethod
    # def create_default(cls, scan_start) -> int:
    #     scan_start_time_index = 1
    #     query = f"INSERT INTO {cls.table_name()} " \
    #             f"({cls.get_model_column_names()[scan_start_time_index]})" \
    #             f" VALUES ({scan_start})"
    #     cls.query(query)
    #     return cls.last_insert_rowid()
