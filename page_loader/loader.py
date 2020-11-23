# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


import os
import re
from typing import Union
from urllib.parse import unquote, urlparse

import requests

ATRIBUTES = ('scheme', 'netloc')
REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
LIMITER_LENGTH_URL = 2000


def get_name_from_url(url: str) -> str:
    """Return the transformed name by pattern."""
    if not url:
        raise ValueError('Missing URL!')

    if len(url) > LIMITER_LENGTH_URL:
        raise ValueError(
            'Your URL has passed the actual limit of {0} characters.'.format(
                LIMITER_LENGTH_URL,
            ),
        )

    url = unquote(url)
    parsed_url = urlparse(url)

    if not all((getattr(parsed_url, atribute) for atribute in ATRIBUTES)):
        raise ValueError("'{0}' string has not scheme or netloc".format(url))

    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    pattern = re.compile(r'\W|_')
    name = re.sub(pattern, REPLACEMENT_SIGN, domain)
    return '{0}{1}'.format(name, EXTENSION)


def scrape(url: str) -> Union[str, bytes]:
    """Pull page content."""
    response = requests.get(url)
    response.raise_for_status()
    if response.encoding:
        return response.text
    return response.content


def download(url: str, directory: str) -> str:
    """Download and save."""
    document = scrape(url)
    name_file = get_name_from_url(url)
    path_to_save = os.path.join(directory, name_file)
    mode = 'w'
    if isinstance(document, bytes):
        mode = 'wb'
    with open(path_to_save, mode=mode) as form:
        form.write(document)
    return path_to_save
