from datetime import datetime

from duplicate_file_removal.database.models.scan_model import ScanModel


def test_create_default(db_path):
    ScanModel.create_table(ScanModel.connect(db_path))
    id = ScanModel.create_default(datetime.now())
    pass
