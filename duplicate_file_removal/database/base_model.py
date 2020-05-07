from typing import List, Tuple
from duplicate_file_removal.logger import logger
from sqlite3 import connect, Connection, Error
from collections import namedtuple


class SQLiteTypes:
    NULL = 'NULL'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    TEXT = 'TEXT'
    BLOB = 'BLOB'


ForeignKey = namedtuple('ForeignKey', 'source_key dst_table foreign_key')


class BaseModel:
    columns: Tuple[Tuple[str, str]] = None
    primary_keys: Tuple[str] = None
    foreign_keys: List[ForeignKey] = None

    @classmethod
    def connect(cls, path: str) -> Connection:
        conn = None
        try:
            conn = connect(path)
        except Error as e:
            logger.error(f"Error while connecting to db '{path}':\n{e}")
        return conn

    @classmethod
    def execute_query(cls, connection: Connection, query: str) -> None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            logger.error(f"Error while executing query '{query}':\n{e}")

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__

    @classmethod
    def create_table(cls, conn: Connection):
        table_creation_query = f"CREATE TABLE {cls.table_name()}" \
                               f"(" \
                               f"{cls.generate_columns()}" \
                               f"{cls.generate_primary_keys()}" \
                               f"{cls.generate_foreign_keys()}" \
                               f");"
        cursor = conn.cursor()
        cursor.execute(table_creation_query)
        conn.commit()

    @classmethod
    def generate_columns(cls) -> str:
        res = ''
        template = "{} {},"
        for column_name, column_type in cls.columns:
            res += template.format(column_name, column_type)

        return res

    @classmethod
    def generate_primary_keys(cls):
        return f"PRIMARY KEY ({tuple(cls.primary_keys)}),"

    @classmethod
    def generate_foreign_keys(cls) -> str:
        res = ''
        template = "FOREIGN KEY ({}) REFERENCES {} ({}),"
        for foreign_key in cls.foreign_keys:
            res += template.format(foreign_key.source_key, foreign_key.dst_table, foreign_key.foreign_key)

        return res
