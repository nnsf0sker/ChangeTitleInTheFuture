import re
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Set
from typing import TypeVar

from lxml import html
from lxml.html import HtmlElement


ReturnType = TypeVar("ReturnType")


def reliable(func: Callable[..., ReturnType]):
    def __new_function(*args, **kwargs) -> Optional[ReturnType]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO: Log work
            pass

    return __new_function


class Parser:
    views_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[1]/ytd-video-view-count-renderer/span[1]"
    date_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[2]/yt-formatted-string"
    likes_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[2]/ytd-toggle-button-renderer[1]/a/yt-formatted-string"
    dislikes_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[2]/ytd-toggle-button-renderer[2]/a/yt-formatted-string"
    comments_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]"
    author_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[7]/div[2]/ytd-video-secondary-info-renderer/div/div/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a"
    title_xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string"

    @staticmethod
    def parse(html_raw: str) -> Dict:
        html_tree = html.fromstring(html_raw)
        return {
            "title": Parser.get_title(html_tree),
            "author_link": Parser.get_author(html_tree),
            "views": Parser.get_views(html_tree),
            "comments": Parser.get_comments(html_tree),
            "date": Parser.get_date(html_tree),
            "likes": Parser.get_likes(html_tree),
            "dislikes": Parser.get_dislikes(html_tree),
            "found_video_ids": Parser.get_video_ids(html_raw),
        }

    @staticmethod
    @reliable
    def get_views(html_tree: HtmlElement) -> int:
        views_tag = Parser.__get_tag_by_xpath(html_tree, Parser.views_xpath)
        views_raw = views_tag.text
        views = int("".join(filter(str.isdecimal, views_raw)))
        return views

    @staticmethod
    @reliable
    def get_author(html_tree: HtmlElement) -> str:
        author_tag = Parser.__get_tag_by_xpath(html_tree, Parser.author_xpath)
        author = author_tag.attrib["href"]
        return author

    @staticmethod
    @reliable
    def get_title(html_tree: HtmlElement) -> str:
        title_tag = Parser.__get_tag_by_xpath(html_tree, Parser.title_xpath)
        title = title_tag.text
        return title

    @staticmethod
    @reliable
    def get_comments(html_tree: HtmlElement) -> int:
        comments_tag = Parser.__get_tag_by_xpath(html_tree, Parser.comments_xpath)
        comments_raw = comments_tag.text
        comments = int("".join(filter(str.isdecimal, comments_raw)))
        return comments

    @staticmethod
    @reliable
    def get_date(html_tree: HtmlElement) -> str:
        date_tag = Parser.__get_tag_by_xpath(html_tree, Parser.date_xpath)
        date_raw = date_tag.text
        # TODO: Доделать обработку теста
        return date_raw

    @staticmethod
    @reliable
    def get_likes(html_tree: HtmlElement) -> int:
        return Parser.get_grades(html_tree, Parser.likes_xpath)

    @staticmethod
    @reliable
    def get_dislikes(html_tree: HtmlElement) -> int:
        return Parser.get_grades(html_tree, Parser.dislikes_xpath)

    @staticmethod
    @reliable
    def get_grades(html_tree: HtmlElement, xpath: str) -> int:
        grades_tag = Parser.__get_tag_by_xpath(html_tree, xpath)
        grades_raw = grades_tag.attrib["aria-label"]
        grades = int("".join(filter(str.isdecimal, grades_raw)))
        return grades

    @staticmethod
    def get_video_ids(html_raw: str) -> Set[str]:
        return set(re.findall(r"/watch\?v=(.{11})", html_raw))

    @staticmethod
    @reliable
    def __get_tag_by_xpath(html_tree: HtmlElement, xpath: str) -> HtmlElement:
        found_tags = html_tree.xpath(xpath)
        if len(found_tags) > 1:
            # TODO: Warning
            pass
        return found_tags[0]
