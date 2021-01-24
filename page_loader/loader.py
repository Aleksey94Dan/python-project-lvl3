# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


import os
import re
from typing import Union
from urllib.parse import unquote, urljoin, urlparse  # noqa: F401

import requests
from bs4 import BeautifulSoup

from page_loader import logging_app

REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
LIMITER_LENGTH_URL = 2000

PATTERN_FOR_STRIP = re.compile(r'(^\W+)|(\W+$)')
PATTERN_FOR_REPLACE = re.compile(r'\b(\W|_)+')
PATTERN_FOR_TAGS = re.compile(r'(link)|(script)|(img)')


logger = logging_app.logger


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
    url = unquote(url)

    try:
        raise_url(url)
    except Exception as err:
        logger.exception('This {0} is incorrect. {1}'.format(url, err))

    url = re.sub(PATTERN_FOR_STRIP, '', url)
    parsed_url = urlparse(url)
    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    url, extension = os.path.splitext(domain)
    name = re.sub(PATTERN_FOR_REPLACE, REPLACEMENT_SIGN, url)
    if any((extension == EXTENSION, extension == '', extension == '.io')):
        return '{0}{1}'.format(name, '.html')
    return '{0}{1}'.format(name, extension)


def scrape(url: str) -> Union[str, bytes]:   # noqa: WPS231, C901
    """Pull page content."""
    response = requests.get(url)
    status_code = response.status_code
    forms: Union[str, bytes] = ''
    try:  # noqa: WPS225
        forms = response.text if response.encoding else response.content
    except requests.RequestException:
        logger.exception(
            'There was an ambiguous exception that occurred while handling'
            'your request: {0}. Error code: {1}'.format(url, status_code),
        )
    except requests.ConnectionError:
        logger.exception(
            'There was an error connecting to URL: {0}.'
            'Error code: {1}'.format(
                url,
                status_code,
            ),
        )
    except requests.HTTPError:
        logger.exception(
            'A Connection error occurred to URL: {0}. Error code: {1}'.format(
                url,
                status_code,
            ),
        )
    except requests.URLRequired:
        logger.exception(
            'Your {0} is invalid. Error code:{1}'.format(
                url,
                status_code,
            ),
        )
    except requests.ConnectTimeout:  # type: ignore
        logger.exception(
            'The request timed out while trying to connect to {0}.'
            'Error code: {1}'.format(url, status_code),
        )
    except requests.ReadTimeout:  # type: ignore
        logger.exception(
            'The {0} did not send any data in the allotted amount of time.'
            'Error code: {1}'.format(url, status_code),
        )
    except requests.Timeout:
        logger.exception(
            'The request timed out. Error code: {0}'.format(status_code),
        )
    return forms


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


def _get_full_url(base_url: str, local_url: str) -> Union[str, None]:
    base_parsed = urlparse(base_url)
    local_parsed = urlparse(local_url)
    if all(  # noqa: WPS337
        (
            base_parsed.scheme == local_parsed.scheme,
            base_parsed.netloc == local_parsed.netloc,
        ),
    ):
        return local_url
    elif not all((local_parsed.scheme, local_parsed.netloc)):  # noqa: WPS504
        return local_url
    return None


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
        url_from_tag = _get_full_url(url, url_from_tag)
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
            write_data(scrape(local_url), os.path.join(directory, local_path))

    path_to_save = os.path.join(directory, base_name)
    write_data(soup.prettify(formatter='html5'), path_to_save)
