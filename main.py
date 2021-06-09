from selenium import webdriver
import time
import re



def get_likes_from_html_raw(html_raw: str) -> int:
    return int("".join(re.findall(
        r'aria-label="([0-9&nbsp;]*) отмет[ок]?[ки]?[ка]? &quot;Нравится&quot;"', html_raw
    )[0].split("&nbsp;")))


def get_dislikes_from_html_raw(html_raw: str) -> int:
    return int("".join(re.findall(
       r'aria-label="([0-9&nbsp;]*) отмет[ок]?[ки]?[ка]? &quot;Не нравится&quot;"', html_raw
    )[0].split("&nbsp;")))


processed_ids = set()

main_queue = {""}

with open("results.csv", "a") as f:
    while main_queue:
        current_id = main_queue.pop()
        url = f"https://youtube.com/watch?v={current_id}"
        likes = -1
        dislikes = -1
        with webdriver.Firefox() as driver:
            driver.get(url)
            time.sleep(10)
            html_raw = driver.page_source
            try:
                found_video_ids = set(re.findall(r"/watch\?v=(.{11})", html_raw))
            except Exception:
                print(f"Error, while taking new YT-links on the page {url}")
            try:
                likes = get_likes_from_html_raw(html_raw)
            except Exception:
                print(f"    Error, while taking likes on the page {url}")
            try:
                dislikes = get_dislikes_from_html_raw(html_raw)
            except Exception:
                f"    Error, while taking dislikes on the page {url}"
            for video_id in found_video_ids:
                if video_id not in processed_ids and video_id not in main_queue:
                    main_queue.add(video_id)
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
