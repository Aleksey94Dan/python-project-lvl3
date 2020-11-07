# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import requests
from itertools import zip_longest


USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'  # noqa: WPS326
)


EXTENSION = '.html'
REPLACEMENT_SIGN = '-'
TAGS = 'link|script|img'


def get_path_to_file(url: str, *, directory: str = '') -> str:
    """Return the transformed name by pattern."""
    parsed_url = urlparse(url)
    domain = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    pattern = re.compile(r'\W|_')
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


def get_url_resourse(path_to_file: str) -> None:
    with open(path_to_file) as html:
        html = html.read()
    only_tags = SoupStrainer(re.compile(TAGS))
    soup = BeautifulSoup(html, "lxml", parse_only=only_tags)
    sripts = soup.find_all('script')
    links = soup.find_all('link')
    imgs = soup.find_all('img')
    urls = []
    for sript in sripts:
        urls.append(sript.get('src'))
    for link in links:
        urls.append(link.get('href'))
    for img in imgs:
        urls.append(img.get('href'))
    urls = list(filter(None, urls))
    print(urls)

if __name__ == "__main__":
    url = 'https://hexlet.io/courses'
    path_to_file = get_path_to_file(url)
    # load(url, path_to_file=path_to_file)
    get_url_resourse(path_to_file)
