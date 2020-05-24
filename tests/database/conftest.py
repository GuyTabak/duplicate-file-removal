from tempfile import TemporaryFile

from pytest import fixture

from duplicate_file_removal.database.models.base_model import BaseModel, SQLiteTypes


@fixture(scope="module")
def db_path():
    f = TemporaryFile(delete=False)
    yield f.name


class MockDBModel(BaseModel):
    columns = (
        ('column_1', SQLiteTypes.INTEGER),
        ('column_2', SQLiteTypes.TEXT),
        ('column_3', SQLiteTypes.NULL),
        ('column_4', SQLiteTypes.BLOB),
        ('column_5', SQLiteTypes.REAL),
    )

    primary_keys = ('column_1', 'column_5')


@fixture(scope="module")
def mock_db_model(db_path):
    model = MockDBModel
    model.DEFAULT_DB_PATH = db_path
    MockDBModel.create_table()
    return model
