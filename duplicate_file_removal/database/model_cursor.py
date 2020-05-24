from sqlite3 import Cursor, Error, Connection
from typing import Tuple, Union, Dict, Optional

from duplicate_file_removal.database.model_queries.model_queries import Query
from duplicate_file_removal.logger import logger


class ModelCursor:
    @classmethod
    def execute(cls, connection: Connection, query_str: str = "", params: Union[Tuple, Dict] = (),
                query_container: Optional[Query] = None, commit=False) -> Cursor:
        """
        Provide either @query_tuple or (@query_tr and @params), if both provided (@query_str and @params) will be used.
        Returns cursor of the executed query on the db_model class.

        Behaviour corresponds to sqlite3 cursor execute style:
         When params is tuple:
            cur.execute("insert into people values (?, ?)", (who, age))
         When param is Dict:
            cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
        :param query_container: sqlite valid query string
        :param params: params to replace any '?' or named var from @query_tuple
        :param query_str: namedtuple Query (query str, params)
        :param connection:
        :param commit: if true, after query execution, connection will be 'committed'
        """
        cursor = connection.cursor()
        # TODO: add test coverage
        if query_container and not query_str:  # If both are provided, query_tuple is ignored.
            query_str = query_container.query
            params = query_container.params

        try:
            # TODO: add test to check if it accepts tuple and dict
            cursor.execute(query_str, params)
            if commit:
                connection.commit()
            return cursor
        except Error as e:
            logger.error(f"Error while executing query '{query_str}':\n{e}")
            raise e

    # TODO (feature): Add fetchone, fetch all and (others?) cursor api to behave in object like manner.
