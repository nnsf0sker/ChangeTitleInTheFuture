import sqlite3

from retry import retry


class ResultsManager:
    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.__connection = self.__establish_connection(self.__db_name)

    def record(
        self,
        video_id: str,
        title: str,
        author_link: str,
        views: int,
        comments: int,
        date: str,
        likes: int,
        dislikes: int,
    ):
        self.__connection.execute(
            "INSERT INTO videos (id, title, author_link, views, comments, date, likes, dislikes) "
            f"VALUES ('{video_id}', '{title}', '{author_link}', {views}, {comments}, '{date}', {likes}, {dislikes});"
        )

    @staticmethod
    @retry(tries=5, delay=1, backoff=2)
    def __establish_connection(db_name: str):
        connection = sqlite3.connect(db_name)
        connection.execute(
            "CREATE TABLE IF NOT EXISTS videos ("
            "id TEXT PRIMARY KEY UNIQUE NOT NULL, "
            "title TEXT, "
            "author_link TEXT, "
            "views BIGINT UNSIGNED, "
            "comments BIGINT UNSIGNED, "
            "date BIGINT UNSIGNED, "
            "likes BIGINT UNSIGNED, "
            "dislikes BIGINT UNSIGNED);"
        )
