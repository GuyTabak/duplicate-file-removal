from collections import namedtuple
from typing import Tuple, List

ForeignKey = namedtuple('ForeignKey', 'source_key dst_table foreign_key')


class BaseModel:
    columns: Tuple[Tuple[str, str]] = None
    primary_keys: Tuple[str] = None
    foreign_keys: Tuple[ForeignKey] = None

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_model_column_names(cls) -> List[str]:
        return [column_name for column_name, _ in cls.columns]
