import logging
import sys
from logging import StreamHandler
from typing import Iterable
from typing import Set

from mysql.connector import connect
from retry import retry

from config import MYSQL_PARSED_ITEMS_ID_COLUMN


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class ParsedItemsManager:
    parsed_item_id_column_name = MYSQL_PARSED_ITEMS_ID_COLUMN

    def __init__(self, host: str, port: int, user: str, password: str, database_name: str, table_name: str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database_name = database_name
        self.__table_name = table_name
        self.__establish_connection()
        self.__parsed_items = self.__full_parsed_items()

    def new_parsed_item(self, video_id: str):
        self.__parsed_items.add(video_id)

    def filter_video_ids(self, video_ids: Iterable[str]) -> Set[str]:
        return set(filter(lambda video_id: video_id not in self.__parsed_items, video_ids))

    @retry(tries=5, delay=1, backoff=2)
    def __full_parsed_items(self) -> Set[str]:
        try:
            self.__cursor.execute(
                f"SELECT {ParsedItemsManager.parsed_item_id_column_name} FROM {self.__database_name}.{self.__table_name}"
            )
            fetched_item = self.__cursor.fetchone()
        except Exception as e:
            logger.error(f"Can't select full items. More: {e}")
            self.__establish_connection()
            raise e
        results = set()
        while fetched_item is not None:
            results.add(fetched_item[0])
            fetched_item = self.__cursor.fetchone()
        return results

    @retry(tries=5, delay=1, backoff=2)
    def __establish_connection(self):
        try:
            self.__db = connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                db=self.__database_name
            )
            self.__cursor = self.__db.cursor()
        except Exception as e:
            logger.error(
                "Can't establish connection to MySQL with parameters: "
                f"host={self.__host}, "
                f"port={self.__port}, "
                f"user={self.__user}, "
                f"password={'*' * len(self.__password)}, "
                f"database_name={self.__database_name}. "
                f"More: {e}"
            )