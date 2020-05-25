from duplicate_file_removal.database.models.scan_model import ScanModel


def insert_scan_start() -> str:
    scan_start_time_index = 1

    return f"INSERT INTO {ScanModel.table_name()} " \
           f"({ScanModel.get_model_column_names()[scan_start_time_index]})" \
           f" VALUES (?)"


def update_scan_completion_time_query() -> str:
    return f"UPDATE {ScanModel.table_name()} " \
           f"SET scan_complete_time = ?" \
           f"WHERE id = ?"
