# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


import os
import re
from typing import Union
from urllib.parse import unquote, urljoin, urlparse  # noqa: F401

import requests
from bs4 import BeautifulSoup

REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
LIMITER_LENGTH_URL = 2000

PATTERN_FOR_STRIP = re.compile(r'(^\W+)|(\W+$)')
PATTERN_FOR_REPLACE = re.compile(r'\b(\W|_)+')
PATTERN_FOR_TAGS = re.compile(r'(link)|(script)|(img)')


def raise_url(url: str) -> None:
    """Raise exceptions caused by URL errors."""
    if not url:
        raise ValueError('Missing URL!')

    if not isinstance(url, str):
        raise TypeError(
            "Incorrectly entered URL! Expected 'str'.",
        )

    if len(url) > LIMITER_LENGTH_URL:
        raise ValueError(
            'Your URL has passed the actual limit of {0} characters.'.format(
                LIMITER_LENGTH_URL,
            ),
        )


def get_name_from_url(url: str) -> str:
    """Return the transformed name by pattern for base url."""
    raise_url(url)

    url = re.sub(PATTERN_FOR_STRIP, '', url)
    parsed_url = urlparse(unquote(url))
    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    url, extension = os.path.splitext(domain)
    name = re.sub(PATTERN_FOR_REPLACE, REPLACEMENT_SIGN, url)
    if any((extension == EXTENSION, extension == '', extension == '.io')):
        return '{0}{1}'.format(name, '.html')
    return '{0}{1}'.format(name, extension)


def scrape(url: str) -> Union[str, bytes]:
    """Pull page content."""
    response = requests.get(url)
    response.raise_for_status()
    if response.encoding:
        return response.text
    return response.content


def write_data(form: Union[str, bytes], path_to_save: str) -> None:
    """Write data along the specified path."""
    mode = 'w'
    if isinstance(form, bytes):
        mode = 'wb'
    with open(path_to_save, mode) as forms:
        forms.write(form)


def get_url_from_src_and_href(tag):
    href = tag.has_attr('href')
    src = tag.has_attr('src')
    if href:
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

    base_document = scrape(url)
    soup = BeautifulSoup(base_document, 'lxml')
    tags = soup.find_all(PATTERN_FOR_TAGS)

    for tag in tags:
        url_from_tag, attr = get_url_from_src_and_href(tag)
        local_path = os.path.join(base_directory, get_name_from_url(url_from_tag))
        tag[attr] = local_path
        local_url = urljoin(url, url_from_tag)
        print(local_url)
        write_data(scrape(local_url), os.path.join(directory, local_path))

    path_to_save = os.path.join(directory, base_name)
    write_data(soup.prettify(formatter='html5'), path_to_save)


if __name__ == "__main__":
    url = 'https://aleksey94dan.github.io/'
    download(url, 'abc')