import time

from retry import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.youtube_page_parser import YouTubePageParser


class Crawler:
    def __init__(self):
        self.__processed_ids = set()
        self.__main_queue = {""}
        self.__driver = Crawler.__set_driver()

    def run(self):
        while self.__main_queue:
            current_id = self.__main_queue.pop()
            url = f"https://youtube.com/watch?v={current_id}"
            likes = -1
            dislikes = -1
            with webdriver.Firefox(options=options) as driver:
                time.sleep(10)


            rate = likes / dislikes
            if rate > 75:
                print(f"[GOOD URL] {url} with [{likes} likes], [{dislikes} dislikes] and [{round(rate, 1)} rate]")
                f.writelines(
                    f"[GOOD URL], {url}, [{likes} likes] [{dislikes} dislikes] [{round(rate, 1)} rate]\n"
                )
            else:
                print(
                    f"     [URL] {url} with [{likes} likes], [{dislikes} dislikes] and [{round(rate, 2)} rate]"
                )
                f.writelines(f"{url}, {likes}, {dislikes}, {round(rate, 2)}\n")
            processed_ids.add(current_id)

    def __process_page(self, url: str) -> None:
        html_raw = self.__get_html_raw(url)
        parsed_info = YouTubePageParser.parse(html_raw)
        time.sleep(10)
        parsed_found_video_ids = parsed_info["found_video_ids"]
        parsed_likes = parsed_info["likes"]
        parsed_dislikes = parsed_info["dislikes"]
        if parsed_likes and parsed_dislikes:
            rate = parsed_likes / parsed_dislikes
        if rate > 75:
            print(f"[GOOD URL] {url} with [{likes} likes], [{dislikes} dislikes] and [{round(rate, 1)} rate]")
            f.writelines(
                f"[GOOD URL], {url}, [{likes} likes] [{dislikes} dislikes] [{round(rate, 1)} rate]\n"
            )
        else:
            print(
                f"     [URL] {url} with [{likes} likes], [{dislikes} dislikes] and [{round(rate, 2)} rate]"
            )
            f.writelines(f"{url}, {likes}, {dislikes}, {round(rate, 2)}\n")
        processed_ids.add(current_id)

    @staticmethod
    def __set_driver():
        options = Options()
        options.headless = True
        return webdriver.Firefox(options=options)

    @retry(tries=5, delay=1, backoff=2)
    def __get_html_raw(self, url) -> str:
        try:
            self.__driver.get(url)
            return self.__driver.page_source
        except Exception as e:
            self.__driver = Crawler.__set_driver()
            raise e
