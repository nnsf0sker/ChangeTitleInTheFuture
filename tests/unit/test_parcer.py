from pathlib import Path

from lxml import html

from core.parser import Parser

current_dir = Path() / "tests" / "unit" / "sample_page.html"

with open(current_dir, "r") as f:
    html_raw = f.read()


parcer = Parser()
html_tree = html.fromstring(html_raw)


# def test_get_title():
#     assert parcer.get_title(html_tree) == "Luis Fonsi - Despacito ft. Daddy Yankee"


def test_get_author():
    assert parcer.get_author(html_tree) == (
        "Luis Fonsi",
        "/channel/UCxoq-PAQeAdk_zyg8YS0JqA",
    )


def test_get_views():
    assert parcer.get_views(html_tree) == 7393954207


def test_get_comments():
    assert parcer.get_comments(html_tree) == 4082675


# def test_get_date():
#     assert parcer.get_date(html_tree) == "13 янв. 2017"


def test_get_likes():
    assert parcer.get_likes(html_tree) == 44515968


def test_get_dislikes():
    assert parcer.get_dislikes(html_tree) == 5055564
