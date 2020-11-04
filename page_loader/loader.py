# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from urllib.parse import urlparse

import requests


def get_name(url: str, replacement_sign: str = '-') -> str:
    """Return the transformed name by pattern."""
    parsed_url = urlparse(url)
    domain = ''.join((parsed_url.netloc, parsed_url.path))
    pattern = re.compile(r'\W|_')
    return ''.join((re.sub(pattern, replacement_sign, domain), '.html'))


def load(url: str, directory: str = '') -> None:
    """Download html document to the specified directory."""
    response = requests.get(url)
    if response.ok:
        name = get_name(url)
        path_to_file = os.path.join(directory, name)
        with open(path_to_file, 'w', encoding='utf-8') as html:
            html.write(response.text)
