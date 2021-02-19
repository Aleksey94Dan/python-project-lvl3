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


def download(url: str, path_to_save: str) -> None:
    """Download and save resource in directory."""
    base_name = my_url.to_name(url)
    base_directory = my_url.to_name(url, directory=True)
    path_to_save_doc = os.path.join(path_to_save, base_name)
    path_to_save_loc = partial(os.path.join, path_to_save, base_directory)
    full_loc_url = partial(my_url.to_full_url, url)
    for_changed_url = _compose(
        partial(os.path.join, base_directory),
        my_url.to_name,
    )
    if not os.path.exists(path_to_save_loc()):
        os.mkdir(path_to_save_loc())

    base_document = scrape.get_content(url)
    prepared_html = parsing.prepare_html(base_document)
    tags = parsing.find_tags(prepared_html)
    urls = parsing.get_urls(tags)
    for index, url in enumerate(urls):
        url = full_loc_url(url)
        tags[index].append(url)
    tags = filter(lambda tag: tag[2] is not None, tags)
    urls = [tag[2] for tag in tags]
    base_document = parsing.modify(prepared_html, tags, for_changed_url)
    store(path_to_save_doc, base_document)
    for url in urls:
        local_doc = scrape.get_content(url)
        local_name = for_changed_url(url)
        store(path_to_save_loc(local_name), local_doc)
