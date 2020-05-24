from collections import namedtuple
from typing import Type

from duplicate_file_removal.database.models.base_model import BaseModel

Query = namedtuple('Query', 'query params')


class ModelQueries:
    _query_separator = ","

    @classmethod
    def create_table_query(cls, db_model: Type[BaseModel]):
        return f"CREATE TABLE {db_model.table_name()} " \
               f"(" \
               f"{cls._generate_columns(db_model)}" \
               f"{cls._generate_primary_keys(db_model)}" \
               f"{cls._generate_foreign_keys(db_model)}" \
               f");"

    @staticmethod
    def last_insert_rowid():
        return "SELECT last_insert_rowid()"

    @classmethod
    def _generate_columns(cls, db_model) -> str:
        template = "{} {}"
        columns = [template.format(column_name, column_type) for column_name, column_type in db_model.columns]
        return f"{cls._query_separator} ".join(columns)

    @classmethod
    def _generate_primary_keys(cls, db_model):
        if not db_model.primary_keys:
            return ""
        return "{} PRIMARY KEY ({})".format(cls._query_separator, cls._query_separator.join(db_model.primary_keys))

    @classmethod
    def _generate_foreign_keys(cls, db_model) -> str:
        res = ""

        if not db_model.foreign_keys:
            return res

        template = "{}FOREIGN KEY ({}) REFERENCES {} ({}) "
        for foreign_key in db_model.foreign_keys:
            res += template.format(cls._query_separator, foreign_key.source_key,
                                   foreign_key.dst_table, foreign_key.foreign_key)

        return res
