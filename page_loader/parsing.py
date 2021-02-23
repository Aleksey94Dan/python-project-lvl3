# -*- coding:utf-8 -*-

"""Parse the page and get local resources."""

import re
from typing import Any, List

import bs4
from bs4 import BeautifulSoup

PATTERN_FOR_TAGS = re.compile(r'(link)|(script)|(img)')
PARSER = 'lxml'
HREF = 'href'
SRC = 'src'
UTF = 'utf-8'
FORMATTER = 'html5'


def prepare_html(html: str) -> bs4.BeautifulSoup:
    """Prepare the page for parsing."""
    return BeautifulSoup(html, PARSER)


def get_urls(tags: List[List]) -> List[str]:
    """Get return urls."""
    if tags:
        return [tag.get(attr) for tag, attr in tags]


def find_tags(
    soup: bs4.BeautifulSoup,
    pattern: re.Pattern = PATTERN_FOR_TAGS,
) -> List[List]:
    """Find specified tags of pattern."""
    tags = soup.find_all(pattern)
    return [
        [tag, HREF] if tag.has_attr(HREF) else [tag, SRC] for tag in tags
    ]


def modify(
    soup: bs4.BeautifulSoup,
    tags: List[List],
    function: Any,
) -> str:
    """Change the content of a tag."""
    if tags:
        for tag, attr, changed_url in tags:
            tag[attr] = function(changed_url)
    return soup.prettify(formatter=FORMATTER)
