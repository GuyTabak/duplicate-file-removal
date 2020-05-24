# This module manages connections, and utilizes db models and model_cursor for this purpose.
from os import remove
from os.path import abspath, sep, expandvars
from sqlite3 import Connection, connect, PARSE_DECLTYPES, PARSE_COLNAMES
from typing import Optional, Type, List

from duplicate_file_removal import PROJECT_NAME
# https://stackoverflow.com/questions/128573/using-property-on-classmethods
# TODO: check multithreading compatability
from duplicate_file_removal.database.model_cursor import ModelCursor
from duplicate_file_removal.database.model_queries.model_queries import ModelQueries
from duplicate_file_removal.database.models.base_model import BaseModel


class DBManager:
    connections = dict()
    # Won't work for unix based systems (%AppData%)
    _DEFAULT_DB_PATH = expandvars(f"%AppData%{sep}{PROJECT_NAME}{sep}db{sep}main_db.sqlite3")

    def __init__(self, path_: Optional[str] = ''):
        self.db_path = abspath(path_) if path_ else self._DEFAULT_DB_PATH

    @property
    def connection(self) -> Connection:
        if self.db_path in self.connections:
            return self.connections[self.db_path]

        connection = self.connect(self.db_path)
        self.connections[self.db_path] = connection

        return connection

    def connect(self, path_: str) -> Connection:
        if path_ in self.connections:
            return self.connections[path_]

        # TODO: understand PARSE_DECLTYPES | PARSE_COLNAMES
        return connect(path_, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)

    def create_table(self, db_model: Type[BaseModel]) -> None:
        ModelCursor.execute(self.connection, query_str=ModelQueries.create_table_query(db_model), commit=True)

    def last_insert_rowid(self) -> str:
        """ returns the ROWID of the last row insert from the database connection"""
        data, _ = ModelCursor.execute(self.connection, ModelQueries.last_insert_rowid()).fetchone()[0]
        return data

    def drop_db(self):
        self.connection.close()
        self.connections.pop(self.db_path)

        remove(self.db_path)

    def initialize_tables(self, db_models: List[Type[BaseModel]]):
        for model in db_models:
            self.create_table(model)
