from itertools import zip_longest
from os import path
from os.path import exists
from tempfile import TemporaryDirectory

from pytest import fixture

from duplicate_file_removal.database.base_model import BaseModel, SQLiteTypes


# NOTE: This test module is building the DB on the go, and preforming operations based on test order.
# 1. DB state should remain the same before and after each individual test with the exception of
#   DB 'structural' operations such as create, drop, etc...

class MockDBModel(BaseModel):
    columns = (
        ('column_1', SQLiteTypes.INTEGER),
        ('column_2', SQLiteTypes.TEXT),
        ('column_3', SQLiteTypes.NULL),
        ('column_4', SQLiteTypes.BLOB),
        ('column_5', SQLiteTypes.REAL),
    )

    primary_keys = ('column_1', 'column_5')


@fixture(scope='module')
def db_path():
    d = TemporaryDirectory()
    path_ = path.join(d.name, "test_db.sqlite3")
    yield path_
    cleanup(path_)


# noinspection PyBroadException
def cleanup(db_path):
    try:
        MockDBModel.drop_db(db_path)
    except:
        pass


@fixture(scope='module')
def db_connection(db_path):
    return BaseModel.connect(db_path)


def test_connect(db_path):
    BaseModel.connect(db_path)
    assert exists(db_path)


def test_create_table(db_connection):
    # Check table created
    MockDBModel.create_table(db_connection)
    table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{MockDBModel.table_name()}';"
    assert MockDBModel.table_name() in MockDBModel.execute_query(db_connection, table_exists_query).fetchone()[0]

    # Check table with expected columns
    cursor = db_connection.execute(f"PRAGMA table_info({MockDBModel.table_name()})")
    columns = cursor.fetchall()
    cursor_name_index = 1
    cursor_type_index = 2
    name_index = 0
    type_index = 1
    # TODO: Check the python-sql lib, it might convert 0 to NULL upon query.
    for cursor_data, mock_data in zip_longest(columns, MockDBModel.columns):
        assert cursor_data[cursor_name_index] == mock_data[name_index]
        if not mock_data[type_index] == "NULL":
            assert cursor_data[cursor_type_index] == mock_data[type_index]
        else:
            assert cursor_data[cursor_type_index] == ""  # Normalize query output


def test_generate_columns():
    for t_1, t_2 in zip_longest(MockDBModel.columns, MockDBModel.generate_columns().split(", ")):
        assert f"{t_1[0]} {t_1[1]}" == t_2
