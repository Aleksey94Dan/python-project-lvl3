# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
from functools import partial
from pathlib import Path
from typing import Union

from page_loader import errors, parsing, scrape
from page_loader import url as my_url

UTF = 'utf-8'


def _compose(g, f):  # noqa: WPS111
    def h(x):  # noqa: WPS111, WPS430
        return g(f(x))
    return h


def store(path_to_save: Path, data: Union[str, bytes]) -> None:  # noqa: WPS110
    """Write data along the specified path."""
    mode, encoding = ('wb', None) if isinstance(data, bytes) else ('w', UTF)
    try:
        with open(path_to_save, mode, encoding=encoding) as out:
            out.write(data)
    except FileNotFoundError as err:
        raise errors.DownloadFileError(
        'This file "{0}" cannot exist.'
        'Try to reduce the length of the filename'.format(path_to_save),
    ) from err


def make_directory(path_to_save: Path) -> None:
    """Create a directory."""
    try:
        if not os.path.exists(path_to_save):
            os.mkdir(path_to_save)
    except PermissionError as err:
        raise errors.DownloadDirectoryError(
        'This file "{0}" cannot write this directory.'.format(
            path_to_save,
        ),
    ) from err


@errors.Supress(errors.DownloadError)
@errors.Supress(errors.DownloadNetworkError)
@errors.Supress(errors.DownloadDirectoryError)
@errors.Supress(errors.DownloadFileError)
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

    links = parsing.get_urls(tags)
    for index, link in enumerate(links):
        tags[index].append(full_loc_url(link))

    tags = list(filter(lambda tag: tag[2] is not None, tags))
    sorted_urls = [url for _, _, url in tags]
    base_document = parsing.modify(prepared_html, tags, for_changed_url)
    store(path_to_save(base_name), base_document)
    for sorted_url in sorted_urls:
        local_doc = scrape.get_content(sorted_url)
        local_name = for_changed_url(sorted_url)
        store(path_to_save(local_name), local_doc)
