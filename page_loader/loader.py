# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os

from typing import Union
from pathlib import Path
from page_loader import url as my_url
from page_loader import scrape
from page_loader import parsing
from functools import partial
from pprint import pprint

def compose(g, f):
    def h(x):
        return g(f(x))
    return h


def store(path_to_save: Path, content: Union[str, bytes]) -> None:
    """Write data along the specified path."""
    with open(path_to_save, 'wb' if isinstance(content, bytes) else 'w') as out:
        out.write(content)


def download(url: str, path_to_save: str) -> None:  # noqa: WPS210
    """Download and save resource in directory."""

    base_name = my_url.to_name(url)
    base_directory = my_url.to_name(url, directory=True)
    path_to_save_doc = os.path.join(path_to_save, base_name)
    path_to_save_loc = partial(os.path.join, path_to_save, base_directory)
    full_loc_url = partial(my_url.to_full_url, url)
    for_changed_url = compose(partial(os.path.join, base_directory), my_url.to_name)
    if not os.path.exists(path_to_save_loc()):
        os.mkdir(path_to_save_loc())

    base_document = scrape.get_content(url)
    prepared_html = parsing.prepare_html(base_document)
    tags = parsing.find_tags(prepared_html)
    urls = parsing.get_urls(tags)
    for i in range(len(urls)):
        url = full_loc_url(urls[i])
        tags[i].append(url)
    tags = filter(lambda tag: tag[2] is not None, tags)
    urls = [tag[2] for tag in tags]
    base_document = parsing.modify(prepared_html, tags, for_changed_url)
    store(path_to_save_doc, base_document)
    for url in urls:
        local_doc = scrape.get_content(url)
        local_name = for_changed_url(url)
        print(local_name)


# download('https://ru.hexlet.io/programs', '/home/aleksey/python-project-lvl3/abc')
