from pathlib import Path

from lxml import html

from core.parser import Parser

sample_page_path = Path(__file__).parent / "sample_page.html"

with open(sample_page_path, "r") as f:
    html_raw = f.read()


parser = Parser()
html_tree = html.fromstring(html_raw)


# def test_get_title():
#     assert parcer.get_title(html_tree) == "Luis Fonsi - Despacito ft. Daddy Yankee"


def test_get_author():
    assert parser.get_author(html_tree) == "/channel/UCxoq-PAQeAdk_zyg8YS0JqA"


def test_get_views():
    assert parser.get_views(html_tree) == 7393954207


def test_get_comments():
    assert parser.get_comments(html_tree) == 4082675


# def test_get_date():
#     assert parcer.get_date(html_tree) == "13 янв. 2017"


def test_get_likes():
    assert parser.get_likes(html_tree) == 44515968


def test_get_dislikes():
    assert parser.get_dislikes(html_tree) == 5055564
