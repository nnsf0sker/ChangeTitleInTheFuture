import re
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Set
from typing import TypeVar
ReturnType = TypeVar("ReturnType")


def reliable(func: Callable[..., ReturnType]):
    def __new_function(*args, **kwargs) -> Optional[ReturnType]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO: Log work
            pass
    return __new_function


class YouTubePageParser:
    @staticmethod
    def parse(html_raw: str) -> Dict[str, Optional[int, Set[str]]]:
        return {
            "dislikes": YouTubePageParser.get_dislikes(html_raw),
            "found_video_ids": YouTubePageParser.get_video_ids(html_raw),
            "likes": YouTubePageParser.get_likes(html_raw)
        }

    @staticmethod
    @reliable
    def get_video_ids(html_raw: str) -> Set[str]:
        return set(re.findall(r"/watch\?v=(.{11})", html_raw))

    @staticmethod
    @reliable
    def get_likes(html_raw: str) -> int:
        return int("".join(re.findall(
            r'aria-label="([0-9&nbsp;]*) отмет[ок]?[ки]?[ка]? &quot;Нравится&quot;"', html_raw
        )[0].split("&nbsp;")))

    @staticmethod
    @reliable
    def get_dislikes(html_raw: str) -> int:
        return int("".join(re.findall(
            r'aria-label="([0-9&nbsp;]*) отмет[ок]?[ки]?[ка]? &quot;Не нравится&quot;"', html_raw
        )[0].split("&nbsp;")))
