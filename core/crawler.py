import time

from retry import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.parser import Parser


class Crawler:
    def __init__(self):
        self.__processed_ids = set()
        self.__main_queue = {""}
        self.__driver = Crawler.__set_driver()

    def run(self):
        with open("results.csv", "a") as results_file:
            while self.__main_queue:
                current_id = self.__main_queue.pop()
                url = f"https://youtube.com/watch?v={current_id}"
                html_raw = self.get_html_raw(url)
                parsed_info = Parser.parse(html_raw)
                time.sleep(10)
                # TODO: Доделать логику
                parsed_found_video_ids = parsed_info["found_video_ids"]
                parsed_likes = parsed_info["likes"]
                parsed_dislikes = parsed_info["dislikes"]
                self.__processed_ids.add(current_id)

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
