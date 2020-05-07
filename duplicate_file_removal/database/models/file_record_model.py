from duplicate_file_removal.database.base_model import BaseModel, SQLiteTypes, ForeignKey


class FileRecordModel(BaseModel):
    columns = (
        ('id', SQLiteTypes.INTEGER),
        ('status', SQLiteTypes.INTEGER),
        ('ext', SQLiteTypes.TEXT),
        ('file_path', SQLiteTypes.TEXT),
        ('hash_value', SQLiteTypes.TEXT),
        ('size', SQLiteTypes.INTEGER),
        ('scan_id', SQLiteTypes.INTEGER)
    )

    primary_keys = ('id',)
    foreign_keys = (ForeignKey('scan_id', 'Scan', 'id'),)
