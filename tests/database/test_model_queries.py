from itertools import zip_longest

from duplicate_file_removal.database.model_queries.model_queries import ModelQueries
from tests.database.conftest import MockDBModel


def test_generate_columns():
    for t_1, t_2 in zip_longest(MockDBModel.columns, ModelQueries._generate_columns(MockDBModel).split(", ")):
        assert f"{t_1[0]} {t_1[1]}" == t_2
