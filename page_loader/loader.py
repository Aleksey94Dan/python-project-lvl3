# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import requests

USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'  # noqa: WPS326
)


EXTENSION: str = '.html'
REPLACEMENT_SIGN: str = '-'


def get_path_to_file(url: str, *, directory: str = '') -> str:
    """Return the transformed name by pattern."""
    parsed_url = urlparse(url)
    domain = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    pattern = re.compile(r'\W|_')
    directory = directory
    name = '{}{}'.format(re.sub(pattern, REPLACEMENT_SIGN, domain), EXTENSION)
    return os.path.join(directory, name)


def load(url: str, *, path_to_file: str = '') -> None:
    """Download html document to the specified directory."""
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.all_ok:
        if response.encoding:
            with open(path_to_file, 'w') as html:
                html.write(response.text)
        else:
            with open(path_to_file, 'wb') as html:
                html.write(response.content)
    else:
        response.raise_for_status()


def has_src(string):
    return string is not None and 'src' in string


def get_resourse(path_to_file: str) -> None:
    with open(path_to_file) as html:
        html = html.read()

    # only_links = SoupStrainer('link', atrr)
    only_scripts = SoupStrainer('script')
    # only_img = SoupStrainer('script')
    soup = BeautifulSoup(html, "html.parser", parse_only=only_scripts)  # for windows
    print(soup.prettify())
    # soup = BeautifulSoup(html, "lxml")  # for linux
    # links = soup.find_all('link')
    # scripts = soup.find_all('script')
    # imgs = soup.find_all('img')
    # pprint(links, scripts, imgs)


if __name__ == "__main__":
    url = 'https://hexlet.io/courses'
    path_to_file = get_path_to_file(url)
    load(url, path_to_file=path_to_file)
    get_resourse(path_to_file)
