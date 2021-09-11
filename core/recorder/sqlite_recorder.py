import sqlite3

from retry import retry

from core.recorder import DBRecorder
from pathlib import Path


class SQLiteRecorder(DBRecorder):
    table = "youtube_parsing_table"

    def __init__(self, db_path: Path):
        self.__db_path = db_path
        self.__connection = SQLiteRecorder.__establish_connection(db_path)
        SQLiteRecorder.__prepare_database(self.__connection)

    def new_record(
            self,
            video_id: str,
            title: str,
            author_id: str,
            views: int,
            comments: int,
            date: str,
            likes: int,
            dislikes: int
    ):
        self.__connection.execute(
            "INSERT INTO videos (id, title, author_id, views, comments, date, likes, dislikes) "
            f"VALUES ('{video_id}', '{title}', '{author_id}', {views}, {comments}, '{date}', {likes}, {dislikes});"
        )

    @staticmethod
    @retry(tries=5, delay=1, backoff=2)
    def __establish_connection(db_name: Path) -> ...:
        connection = sqlite3.connect(db_name)
        return connection

    @staticmethod
    def __prepare_database(connection):
        connection.execute(
            f"CREATE TABLE IF NOT EXISTS {SQLiteRecorder.table} ("
            "id TEXT PRIMARY KEY UNIQUE NOT NULL, "
            "title TEXT, "
            "author_id TEXT, "
            "views BIGINT UNSIGNED, "
            "comments BIGINT UNSIGNED, "
            "date BIGINT UNSIGNED, "
            "likes BIGINT UNSIGNED, "
            "dislikes BIGINT UNSIGNED);"
        )
