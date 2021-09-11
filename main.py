import logging
import sys
from logging import StreamHandler

from config import MYSQL_HOST
from config import MYSQL_PARSED_ITEMS_DATABASE
from config import MYSQL_PARSED_ITEMS_TABLE
from config import MYSQL_PASSWORD
from config import MYSQL_PORT
from config import MYSQL_USER
from core.crawler import Crawler
from core.parsed_items_manager import ParsedItemsManager
from core.recorder.mysql_recorder import MySQLRecorder


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


if __name__ == "__main__":
    logger.info("Script preparations has been started...")

    mysql_recorder = MySQLRecorder(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database_name=MYSQL_PARSED_ITEMS_DATABASE,
        table_name=MYSQL_PARSED_ITEMS_TABLE
    )
    logger.debug(
        "MySQLRecorder has been successfully initialised with parameters: "
        f"host={MYSQL_HOST}, "
        f"port={MYSQL_PORT}, "
        f"user={MYSQL_USER}, "
        f"password={'*' * len(MYSQL_PASSWORD)}, "
        f"database_name={MYSQL_PARSED_ITEMS_DATABASE}, "
        f"table_name={MYSQL_PARSED_ITEMS_TABLE}"
    )

    parsed_items_manager = ParsedItemsManager(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database_name=MYSQL_PARSED_ITEMS_DATABASE,
        table_name=MYSQL_PARSED_ITEMS_TABLE
    )
    logger.debug(
        "ParsedItemsManager has been successfully initialised with parameters: "
        f"host={MYSQL_HOST}, "
        f"port={MYSQL_PORT}, "
        f"user={MYSQL_USER}, "
        f"password={'*' * len(MYSQL_PASSWORD)}, "
        f"database_name={MYSQL_PARSED_ITEMS_DATABASE}, "
        f"table_name={MYSQL_PARSED_ITEMS_TABLE}"
    )

    crawler = Crawler(recorder=mysql_recorder, parsed_items_manager=parsed_items_manager)
    logger.info("Script preparations has been successfully finished.")

    logger.info("Starting script...")
    crawler.run()
