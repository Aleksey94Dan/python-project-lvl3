# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""

import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import requests
from pprint import pprint


USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'  # noqa: WPS326
)

REPLACEMENT_SIGN = '-'
TAGS = 'link|script|img'


def get_name(url: str) -> str:
    """Return the transformed name by pattern."""
    parsed_url = urlparse(url)
    domain = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    domain, extension = os.path.splitext(domain)
    if extension == '':
        extension = '.html'
    pattern = re.compile(r'\W|_')
    name = re.sub(pattern, REPLACEMENT_SIGN, domain)
    return '{}{}'.format(name, extension)


def has_domain(url):
    if url is None:
        return False
    parse_uri = urlparse(url)
    if parse_uri.netloc:
        return True
    return False

def get_directory(name: str, *, directory: str = ''):
    name, extension = os.path.splitext(name)
    if extension == '.html':
        name = '{}{}'.format(name, '_files')
    path_to_dir = os.path.join(directory, name)
    if os.path.exists(path_to_dir):
        return path_to_dir
    else:
        os.makedirs(path_to_dir)
        return path_to_dir



def load(url: str, *, directory: str = '') -> None:
    """Download html document to the specified directory."""
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.all_ok:
        if response.encoding:
            name = get_name(url)
            path_to_file = os.path.join(directory, name)
            with open(path_to_file, 'w') as html:
                html.write(response.text)
        else:
            with open(path_to_file, 'wb') as html:
                html.write(response.content)
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
    urls = list(filter(has_domain, urls))
    return urls



if __name__ == "__main__":
    url = 'https://hexlet.io/courses'
    name = get_name(url)
    path_to_save = 'abc'
    load(url, directory=path_to_save)
    directory_for_locale = get_directory(name, directory=path_to_save)
    print(directory_for_locale)

    # print(name)
    # directory = os.path.join(path_to_save, get_directory(name))
    # print(directory)
