# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from urllib.parse import urlparse

import requests

USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',  # noqa: WPS326
)


def get_name(url: str, replacement_sign: str = '-') -> str:
    """Return the transformed name by pattern."""
    parsed_url = urlparse(url)
    domain = ''.join((parsed_url.netloc, parsed_url.path))
    pattern = re.compile(r'\W|_')
    return ''.join((re.sub(pattern, replacement_sign, domain), '.html'))


def load(url: str, directory: str = '') -> None:
    """Download html document to the specified directory."""
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.ok:
        name = get_name(url)
        path_to_file = os.path.join(directory, name)
        with open(path_to_file, 'w') as html:
            html.write(response.text)
