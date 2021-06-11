import re
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from core.youtube_page_parser import YouTubePageParser

processed_ids = set()

main_queue = {""}

options = Options()
options.headless = True

with open("results.csv", "a") as f:
    while main_queue:
        current_id = main_queue.pop()
        url = f"https://youtube.com/watch?v={current_id}"
        likes = -1
        dislikes = -1
        with webdriver.Firefox(options=options) as driver:
            driver.get(url)
            time.sleep(10)
            html_raw = driver.page_source
            parsed_info = YouTubePageParser.parse(html_raw)
            
        rate = likes/dislikes
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
