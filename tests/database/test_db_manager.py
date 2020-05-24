from itertools import zip_longest

from tests.database.conftest import MockDBModel


def test_create_table(db_manager):
    # Check table created
    db_manager.safe_create_table(MockDBModel)
    table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{MockDBModel.table_name()}';"
    assert MockDBModel.table_name() in db_manager.connection.execute(table_exists_query).fetchone()[0]

    # Check table with expected columns
    cursor = db_manager.connection.execute(f"PRAGMA table_info({MockDBModel.table_name()})")
    columns = cursor.fetchall()

    for cursor_data, mock_data in zip_longest(columns, MockDBModel.columns):
        name, type_ = mock_data
        cursor_name, cursor_type = cursor_data[1:3]

        assert name == cursor_name
        if not type_ == "NULL":
            assert type_ == cursor_type
        else:
            assert cursor_type == ""  # Normalize query output
