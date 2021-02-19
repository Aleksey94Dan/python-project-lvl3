# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
from functools import partial
from pathlib import Path
from typing import Union

from page_loader import parsing, scrape
from page_loader import url as my_url


def _compose(g, f):  # noqa: WPS111
    def h(x):  # noqa: WPS111, WPS430
        return g(f(x))
    return h


def store(path_to_save: Path, data: Union[str, bytes]) -> None:  # noqa; WPS110
    """Write data along the specified path."""
    with open(path_to_save, 'wb' if isinstance(data, bytes) else 'w') as out:
        out.write(data)


def make_directory(path_to_save: Path) -> None:
    """Create a directory."""
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)


def download(url: str, path_to_save: str) -> None:  # noqa: WPS210
    """Download and save resource in directory."""
    base_name = my_url.to_name(url)
    base_directory = my_url.to_name(url, directory=True)
    path_to_save = partial(os.path.join, path_to_save)
    full_loc_url = partial(my_url.to_full_url, url)
    for_changed_url = _compose(
        partial(os.path.join, base_directory),
        my_url.to_name,
    )

    make_directory(path_to_save(base_directory))

    base_document = scrape.get_content(url)
    prepared_html = parsing.prepare_html(base_document)
    tags = parsing.find_tags(prepared_html)
    urls = parsing.get_urls(tags)
    for index, url in enumerate(urls):
        url = full_loc_url(url)
        tags[index].append(url)

    tags = list(filter(lambda tag: tag[2] is not None, tags))
    urls = [url for _, _, url in tags]
    base_document = parsing.modify(prepared_html, tags, for_changed_url)
    store(path_to_save(base_name), base_document)
    for url in urls:
        local_doc = scrape.get_content(url)
        local_name = for_changed_url(url)
        store(path_to_save(local_name), local_doc)
