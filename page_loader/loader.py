# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


import os
import re
from typing import Union
from urllib.parse import unquote, urlparse, urljoin
from bs4 import BeautifulSoup
import requests

ATRIBUTES = ('scheme', 'netloc')
REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
LIMITER_LENGTH_URL = 2000

def get_name_for_local_resource(url: str) -> str:
    name, extension = os.path.splitext(url)
    name = name.strip('/')
    pattern = re.compile(r'\b(\W|_)+')
    name = re.sub(pattern, REPLACEMENT_SIGN, name)
    return '{0}{1}'.format(name, extension)


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

    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path).strip('/')
    pattern = re.compile(r'\b(\W|_)+')
    name = re.sub(pattern, REPLACEMENT_SIGN, domain)
    return '{0}{1}'.format(name, EXTENSION)


def scrape(url: str) -> Union[str, bytes]:
    """Pull page content."""
    response = requests.get(url)
    response.raise_for_status()
    if response.encoding:
        return response.text
    return response.content


def download(url: str, directory: str) -> str:  # noqa: WPS210
    """Download and save."""
    base_document = scrape(url)
    base_name = get_name_from_url(url)
    path_to_save = os.path.join(directory, base_name)

    if base_name.endswith('.html'):
        base_directory = path_to_save.replace('.html', '_files')
        if not os.path.exists(base_directory):
            os.mkdir(base_directory)

    with open(path_to_save, 'w') as form:
        form.write(base_document)

    # soup = BeautifulSoup(base_document, 'lxml')
    # img = soup.find('img')
    # img_url = urljoin(url, img.get('src'))

    # content = scrape(img_url)
    # name_content = get_name_for_local_resource(img.get('src'))
    # path_to_save = os.path.join(base_directory, name_content)
    # print(path_to_save)

    # with open(path_to_save, 'wb') as f:
    #     f.write(content)

    # return path_to_save


if __name__ == "__main__":
    download('https://aleksey94dan.github.io/', 'abc' )