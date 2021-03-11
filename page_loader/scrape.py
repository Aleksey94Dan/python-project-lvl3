# -*- coding:utf-8 -*-

"""The module sends HTTP requests to the content."""


from typing import Union

import requests
from requests.exceptions import (
    ConnectionError,
    InvalidSchema,
    InvalidURL,
    MissingSchema,
)

from page_loader import errors
from functools import wraps
from progress.bar import Bar

from progress.bar import IncrementalBar

def progress_bar(function):
    @wraps(function)
    def wrapped(args):
        gen = function(args)
        content = next(gen)
        suffix = '%(percent)d%% [%(elapsed_td)s / %(eta)d / %(eta_td)s]'
        with IncrementalBar(args, suffix = suffix, max=200) as bar:
            for i in gen:
                bar.next()
                content += i
        return content
    return wrapped


@progress_bar
def get_content(url: str) -> Union[str, bytes]:
    """Pull page content."""
    try:  # noqa: WPS225
        response = requests.get(url, stream=True)
    except ConnectionError as err1:
        raise errors.DownloadError(
            'An error occurred connecting to {0}'.format(url),
        ) from err1
    except MissingSchema as err2:
        raise errors.DownloadError(
            'Your missed the "http/https" in url: {0}'.format(url),
        ) from err2
    except InvalidSchema as err3:
        raise errors.DownloadError(
            'You have the wrong scheme in url: {0}'.format(url),
        ) from err3
    except InvalidURL as err4:
        raise errors.DownloadError(
            'You entered an invalid url: {0}'.format(url),
        ) from err4
    response.raise_for_status()
    if response.encoding is None:
        response.encoding = 'utf-8'
    return response.iter_content(decode_unicode=True)


print(get_content('https://habr.com/ru/'))
