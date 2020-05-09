from itertools import zip_longest
from os import path
from os.path import exists
from tempfile import TemporaryDirectory

from duplicate_file_removal.database.base_model import BaseModel, SQLiteTypes
from pytest import fixture


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

    primary_keys = ('column_1',)


@fixture(scope='module')
def db_path():
    d = TemporaryDirectory()
    yield path.join(d.name, "'test_db.sqlite3")


@fixture(scope='module')
def db_connection(db_path):
    return BaseModel.connect(db_path)


def test_connect(db_path):
    BaseModel.connect(db_path)
    assert exists(db_path)


def test_create_table(db_connection):
    MockDBModel.create_table(db_connection)
    table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name={MockDBModel.table_name()};"
    assert MockDBModel.execute_query(db_connection, table_exists_query)

    table_columns_query = f"SELECT sql FROM sqlite_master WHERE tbl_name = {MockDBModel.table_name()} AND type = 'table'"
    # TODO: check what PRAGMA table_info(table_name) is.


def test_generate_columns():
    for t_1, t_2 in zip_longest(MockDBModel.columns, MockDBModel.generate_columns()[:-1]):
        assert f"{t_1[0]} {t_1[1]}," == t_2




def test_drop_db(db_path):
    # HAS TO BE LAST
    BaseModel.drop_db(db_path)
    assert not exists(db_path)
