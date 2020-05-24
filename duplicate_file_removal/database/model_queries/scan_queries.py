from datetime import datetime

from duplicate_file_removal.database.models.scan_model import ScanModel


def insert_scan_start():
    scan_start_time_index = 1

    return f"INSERT INTO {ScanModel.table_name()} " \
           f"({ScanModel.get_model_column_names()[scan_start_time_index]})" \
           f" VALUES (?)"
