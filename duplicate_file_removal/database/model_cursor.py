from logging import Logger
from sqlite3 import Cursor, Error, Connection
from typing import Tuple, Union, Dict, Optional


def execute(connection: Connection, query_str: str, params: Union[Tuple, Dict] = (), commit=False,
            logger_: Optional[Logger] = None) -> Cursor:
    """
        Wraps sqlite Cursor.execute with logging

    :param params: params to replace any '?' or named var from @query_tuple
    :param query_str: namedtuple Query (query str, params)
    :param connection:
    :param commit: if true, after query execution, connection will be 'committed'
    :param logger_: optional logger to enable logging in case of exception
    """
    cursor = connection.cursor()

    try:
        cursor.execute(query_str, params)
        if commit:
            connection.commit()
        return cursor
    except Error as e:
        if logger_:
            logger_.error(f"Error while executing query '{query_str}':\n{e}")
        raise e
