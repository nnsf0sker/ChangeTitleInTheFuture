import logging
import sys
import time
from logging import StreamHandler
import re

from retry import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.parsed_items_manager import ParsedItemsManager
from core.parser import Parser
from core.recorder import DBRecorder

x = re.sub

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

WARNINGS_LIMIT = 10


class Crawler:
    def __init__(self, recorder: DBRecorder, parsed_items_manager: ParsedItemsManager):
        self.__main_queue = {""}
        logger.info(f"Main queue is set to {self.__main_queue}")
        logger.info("Setting browser driver...")
        self.__driver = Crawler.__set_driver()
        logger.info("Browser driver has been successfully set")
        self.__recorder = recorder
        self.__parsed_items_manager = parsed_items_manager

    def run(self):
        logger.info("Starting crawling...")
        step_number = 1
        warnings = 0
        while self.__main_queue:
            video_id = self.__main_queue.pop()
            url = f"https://youtube.com/watch?v={video_id}"
            logger.info(f"Processing {url} ...")
            html_raw = self.get_html_raw(url)
            parsed_info = Parser.parse(html_raw)
            title = parsed_info["title"]
            author_id = parsed_info["author_id"]
            found_video_ids = parsed_info["found_video_ids"]
            views = parsed_info["views"]
            likes = parsed_info["likes"]
            dislikes = parsed_info["dislikes"]
            comments = parsed_info["comments"]
            date = parsed_info["date"]
            if not (title and views and comments and likes and dislikes):
                warnings += 1
                if warnings >= WARNINGS_LIMIT:
                    raise Exception("Too many warnings!")
            else:
                warnings = 0
            logger.info(
                f"Step [{step_number:5.0f}] | URL: {url}:\n"
                f'    "title" == {title}\n'
                f'    "author_id" == {author_id}\n'
                f'    "views" == {views}\n'
                f'    "likes" == {likes}\n'
                f'    "dislikes" == {dislikes}\n'
                f'    "comments" == {comments}\n'
                f'    "date" == {date}\n'
                f'    len(found_video_ids) == {len(found_video_ids)}\n'
                f'    Main queue length = {len(self.__main_queue)}\n'
                f'    Warnings count = {warnings}\n'
            )
            try:
                self.__recorder.new_record(
                    video_id=video_id,
                    title=title,
                    author_id=author_id,
                    views=views,
                    comments=comments,
                    date=date,
                    likes=likes,
                    dislikes=dislikes
                )
            except Exception as e:
                print(e)
            self.__parsed_items_manager.new_parsed_item(video_id)
            new_video_ids = self.__parsed_items_manager.filter_video_ids(found_video_ids)
            if len(self.__main_queue) > 1000:
                self.__main_queue = set(new_video_ids)
                logger.info(f"Empting 'main_queue'. Now it is set to {set(new_video_ids)}")
            else:
                self.__main_queue.update(new_video_ids)
            step_number += 1
            time.sleep(5)

    @staticmethod
    def __set_driver():
        options = Options()
        options.headless = True
        return webdriver.Firefox(options=options)

    @retry(tries=5, delay=1, backoff=2)
    def get_html_raw(self, url) -> str:
        try:
            self.__driver.get(url)
            for i in range(15):
                self.__driver.execute_script(f"window.scrollTo(0, {100 * i})")
            return self.__driver.page_source
        except Exception as e:
            self.__driver = Crawler.__set_driver()
            raise e
