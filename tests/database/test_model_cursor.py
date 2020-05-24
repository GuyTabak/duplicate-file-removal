from random import getrandbits, random

from pytest import fixture

from duplicate_file_removal.database.model_cursor import ModelCursor


@fixture(scope="module")
def insert_query() -> str:
    return ""


def test_execute_with_tuple_params(mock_db_model):
    table_name = mock_db_model.table_name()
    params = ('text', None, getrandbits(10), random())
    ModelCursor.execute(mock_db_model, query_str=f"INSERT INTO {table_name}(column_2, column_3, column_4, column_5)"
                                                 f" VALUES (?, ?, ?, ?)", params=params, commit=True)

    row = mock_db_model.last_insert_rowid()
    row_data = ModelCursor.execute(mock_db_model, f"SELECT * FROM {table_name} WHERE rowid = ?;", params=(row,),
                                   commit=True)
    assert row_data.fetchone()[1:] == params  # skip rowid column


def test_execute_with_dict_params(mock_db_model):
    table_name = mock_db_model.table_name()
    params = {'val_2': 'some text', 'val_3': None, 'val_4': getrandbits(10), 'val_5': random()}
    ModelCursor.execute(mock_db_model, query_str=f"INSERT INTO {table_name}(column_2, column_3, column_4, column_5)"
                                                 f" VALUES (:val_2, :val_3,"
                                                 f" :val_4, :val_5)",
                        params=params, commit=True)

    row = mock_db_model.last_insert_rowid()
    row_data = ModelCursor.execute(mock_db_model, f"SELECT * FROM {table_name} WHERE rowid=:rowid;",
                                   params={'rowid': row}, commit=True)
    assert row_data.fetchone()[1:] == tuple(value for key, value in params.items())  # skip rowid column
