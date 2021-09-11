import logging
import sys
from logging import StreamHandler

from mysql.connector import connect
from retry import retry

from core.recorder import DBRecorder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class MySQLRecorder(DBRecorder):
    def __init__(self, host: str, port: int, user: str, password: str, database_name: str, table_name: str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database_name = database_name
        self.__table_name = table_name
        self.__establish_connection()

    @retry(tries=5, delay=1, backoff=2)
    def new_record(
            self,
            video_id: str,
            title: str,
            author_id: str,
            views: int,
            comments: int,
            date: str,
            likes: int,
            dislikes: int,
    ):
        try:
            if video_id:
                self.__cursor.execute(
                    f"REPLACE INTO {self.__database_name}.{self.__table_name} ("
                    f"video_id, title, author_id, views, comments, date, likes, dislikes"
                    f") VALUES ("
                    f"'{video_id}', "
                    f"'{title or 'NULL'}', "
                    f"'{author_id or 'NULL'}', "
                    f"{views or 'NULL'}, "
                    f"{comments or 'NULL'}, "
                    f"'{date or 'NULL'}', "
                    f"{likes or 'NULL'}, "
                    f"{dislikes or 'NULL'}"
                    f");"
                )
                self.__db.commit()
                logger.info(f"MySQLRecorder new record (video_id={video_id})")
        except Exception as e:
            logger.warning(f"MySQLRecorder can't create new record (video_id={video_id}). More: {e}")
            self.__establish_connection()
            raise e

    @retry(tries=5, delay=1, backoff=2)
    def __establish_connection(self):
        try:
            self.__db = connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                database=self.__database_name
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

    def __del__(self):
        self.__cursor.close()
        self.__db.close()
