from duplicate_file_removal.database.models.scan_model import ScanModel


def test_create_default(db_manager):
    db_manager.create_table(ScanModel)
    pass
