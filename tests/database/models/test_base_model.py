from tests.database.conftest import MockDBModel


def test_get_model_column_names():
    for column_name, _ in MockDBModel.columns:
        assert column_name in MockDBModel.get_model_column_names()
