from config import RESULTS_DATABASE_PATH

from core.crawler import Crawler
from core.recorder import Recorder


if __name__ == "__main__":
    recorder = Recorder(db_path=RESULTS_DATABASE_PATH)
    crawler = Crawler(recorder)
    crawler.run()
