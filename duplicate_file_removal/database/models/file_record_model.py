from duplicate_file_removal.database.models.base_model import BaseModel, ForeignKey
from duplicate_file_removal.database.models.scan_model import ScanModel
from duplicate_file_removal.database.types import SQLiteTypes


class FileRecordModel(BaseModel):
    columns = (
        ('id', SQLiteTypes.INTEGER),
        ('ext', SQLiteTypes.TEXT),
        ('file_path', SQLiteTypes.TEXT),
        ('hash_value', SQLiteTypes.TEXT),
        ('size', SQLiteTypes.INTEGER),
        ('scan_id', SQLiteTypes.INTEGER)
    )

    primary_keys = ('id', 'scan_id')
    foreign_keys = (ForeignKey('scan_id', ScanModel.table_name(), 'id'),)
