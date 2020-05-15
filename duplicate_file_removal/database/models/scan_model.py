from enum import Enum

from duplicate_file_removal.database.base_model import BaseModel, SQLiteTypes


class ScanStatus(Enum):
    initiated, completed = range(2)


class ScanModel(BaseModel):
    columns = (
        ('id', SQLiteTypes.INTEGER),
        ('scan_start_time', SQLiteTypes.REAL),
        ('scan_complete_time', SQLiteTypes.REAL),
        ('scan_status', SQLiteTypes.TEXT)
    )
    primary_keys = ('id',)

    # TODO: test
    @classmethod
    def create(cls, scan_start) -> int:
        scan_start_time_index = 1
        query = f"INSERT INTO {cls.table_name()} ({cls.get_model_column_names()[scan_start_time_index]})" \
                f"VALUES{scan_start}"
        res = cls.query(query)  # TODO: See if i can return id
        return res.next()
