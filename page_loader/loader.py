# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


import os
import re
from typing import Union
from urllib.parse import unquote, urljoin, urlparse

import requests
import requests_mock
from bs4 import BeautifulSoup, SoupStrainer

REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
LIMITER_LENGTH_URL = 2000
PATTERN_FOR_STRIP = re.compile(r'(^\W+)|(\W+$)')
PATTERN_FOR_REPLACE = re.compile(r'\b(\W|_)+')


def raise_url(url: str) -> None:
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
    if any((extension == EXTENSION, extension == '')):
        return '{0}{1}'.format(name, '.html')
    return '{0}{1}'.format(name, extension)


def scrape(url: str) -> Union[str, bytes]:
    """Pull page content."""
    response = requests.get(url)
    response.raise_for_status()
    if response.encoding:
        return response.text
    return response.content


# def download(url: str, directory: str) -> None:  # noqa: WPS210
#     """Download and save."""
#     base_document = scrape(url)
#     base_name = get_name_from_url(url)
#     path_to_save = os.path.join(directory, base_name)

#     if base_name.endswith('.html'):
#         base_directory = path_to_save.replace('.html', '_files')
#         if not os.path.exists(base_directory):
#             os.mkdir(base_directory)
#     soup = BeautifulSoup(base_document, 'lxml')
#     tags = soup.find_all(re.compile(r'(link)|(script)|(img)'))

#     for tag in tags:
#         src = tag.get('src')
#         href = tag.get('href')
#         _, base_directory = os.path.split(base_directory)
#         if src:
#             local_url = os.path.join(base_directory, get_name_for_local_resource(src))
#             tag['src'] = local_url
#         if href:
#             local_url = os.path.join(base_directory, get_name_for_local_resource(href))
#             tag['href'] = local_url
#     print(soup)
    # img = soup.find('img')
    # url_img = img.get('src')
    # _, base_directory = os.path.split(base_directory)
    # local_url = os.path.join(
    #     base_directory,
    #     get_name_for_local_resource(url_img),
    # )
    # print(local_url)
    # img['src'] = local_url

    # with open(path_to_save, 'w') as form:
    #     form.write(soup.prettify(formatter='html5'))

    # new_url = urljoin(url, url_img)
    # image = scrape(new_url)
    # path_to_save = os.path.join(directory, local_url)
    # if isinstance(image, bytes):
    #     with open(path_to_save, 'wb') as f_img:
    #         f_img.write(image)



if __name__ == "__main__":
    from pprint import pprint
#     with open('tests/fixture/site/index.html') as html:
#         FORMS = html.read()
#     BASE_URL = 'https://ru.hexlet.io/courses'
#     with requests_mock.Mocker() as m:
#         m.get(BASE_URL, text=FORMS)
# #         download(BASE_URL, 'abc')
#     with open('tests/fixture/actual_base_urls') as f_urls:
#         urls = f_urls.readlines()
#     new_urls = list(map(get_name_from_url, urls))
    # pprint(new_urls)
    print(get_name_from_url('asdfkljasdkf'))
