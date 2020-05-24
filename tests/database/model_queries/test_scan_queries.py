from duplicate_file_removal.database.model_queries.scan_queries import insert_scan_start
from duplicate_file_removal.database.models.scan_model import ScanModel
from duplicate_file_removal.database.model_cursor import execute
from datetime import datetime


def test_insert_scan_start(db_manager):
    db_manager.safe_create_table(ScanModel)

    start = datetime.now()
    query = insert_scan_start()
    execute(db_manager.connection, query, (start,))

    res = execute(db_manager.connection, f"SELECT * FROM {ScanModel.table_name()} WHERE scan_start_time = ?", (start,),
                  commit=True).fetchone()
    assert res is not None
