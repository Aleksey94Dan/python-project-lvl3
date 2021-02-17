# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from typing import Union

import requests
from bs4 import BeautifulSoup


def write_data(form: Union[str, bytes], path_to_save: str) -> None:
    """Write data along the specified path."""
    mode = 'w'
    if isinstance(form, bytes):
        mode = 'wb'
    with open(path_to_save, mode) as forms:
        forms.write(form)


def _get_url_from_src_and_href(tag):
    if tag.has_attr('href'):
        return tag.get('href'), 'href'
    return tag.get('src'), 'src'




def download(url: str, directory: str) -> None:  # noqa: WPS210
    """Download and save resource in directory."""
    base_name = get_name_from_url(url)
    base_directory = base_name.replace(EXTENSION, '_files')

    if base_name.endswith(EXTENSION):
        local_directory = os.path.join(directory, base_directory)
        if not os.path.exists(local_directory):
            os.mkdir(local_directory)
    logger.debug(
        'This page {0} downloaded here {1}'.format(
            url,
            os.path.abspath(directory),
        ),
    )
    base_document = scrape(url)
    soup = BeautifulSoup(base_document, 'lxml')
    tags = soup.find_all(PATTERN_FOR_TAGS)

    for tag in tags:
        url_from_tag, attr = _get_url_from_src_and_href(tag)
        url_from_tag = _check_adapter(_get_full_url(url, url_from_tag))
        if url_from_tag:
            local_url = urljoin(url, url_from_tag)
            local_path = os.path.join(
                base_directory,
                get_name_from_url(local_url),
            )
            logger.debug(
                'These local sources {0} downloaded here {1}'.format(
                    local_url,
                    os.path.abspath(local_path),
                ),
            )
            tag[attr] = local_path
            write_data(
                scrape(local_url),
                os.path.join(directory, local_path),
            )
    path_to_save = os.path.join(directory, base_name)
