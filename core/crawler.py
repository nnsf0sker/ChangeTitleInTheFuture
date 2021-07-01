import time

from retry import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.parser import Parser
from core.recorder import Recorder


class Crawler:
    def __init__(self, recorder: Recorder):
        self.__processed_ids = set()
        self.__main_queue = {""}
        self.__driver = Crawler.__set_driver()
        self.__recorder = recorder

    def run(self):
        while self.__main_queue:
            current_id = self.__main_queue.pop()
            url = f"https://youtube.com/watch?v={current_id}"
            html_raw = self.get_html_raw(url)
            parsed_info = Parser.parse(html_raw)
            time.sleep(10)
            # TODO: Доделать логику
            title = parsed_info["title"]
            author_link = parsed_info["author_link"]
            found_video_ids = parsed_info["found_video_ids"]
            views = parsed_info["views"]
            likes = parsed_info["likes"]
            dislikes = parsed_info["dislikes"]
            comments = parsed_info["comments"]
            date = parsed_info["date"]
            self.__recorder.record(
                video_id=current_id,
                title=title,
                author_link=author_link,
                views=views,
                comments=comments,
                date=date,
                likes=likes,
                dislikes=dislikes
            )
            print(
                f"{current_id}, {views}, {likes}, {dislikes}, {comments}, {title}, {author_link}"
            )
            self.__processed_ids.add(current_id)
            self.__main_queue.update(
                filter(
                    lambda video_id: video_id not in self.__processed_ids,
                    found_video_ids,
                )
            )

    @staticmethod
    def __set_driver():
        options = Options()
        options.headless = True
        return webdriver.Firefox(options=options)

    @retry(tries=5, delay=1, backoff=2)
    def get_html_raw(self, url) -> str:
        try:
            self.__driver.get(url)
            for i in range(10):
                self.__driver.execute_script(f"window.scrollTo(0, {100 * i})")
            return self.__driver.page_source
        except Exception as e:
            self.__driver = Crawler.__set_driver()
            raise e
