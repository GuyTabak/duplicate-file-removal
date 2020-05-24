from enum import Enum

from duplicate_file_removal.database.models.base_model import BaseModel
from duplicate_file_removal.database.types import SQLiteTypes


class ScanStatus(Enum):
    initiated, completed = range(2)


class ScanModel(BaseModel):
    # TODO: consider metaclass to allow access columns in pythonic way .*
    columns = (
        ("id", SQLiteTypes.INTEGER),
        ("scan_start_time", "timestamp"),
        ("scan_complete_time", "timestamp"),
        ("scan_status", "TEXT")
    )
    primary_keys = ('id',)
