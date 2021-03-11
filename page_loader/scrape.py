# -*- coding:utf-8 -*-

"""The module sends HTTP requests to the content."""
from functools import wraps
from typing import Union

import requests
from progress.spinner import LineSpinner
from requests.exceptions import (
    ConnectionError,
    InvalidSchema,
    InvalidURL,
    MissingSchema,
)

from page_loader import errors


def progress_bar(function):  # noqa: D103
    @wraps(function)  # noqa: WPS430
    def wrapped(args):
        with LineSpinner(args) as pb_bar:
            lines = function(args)
            acc = next(lines)
            for line in lines:
                acc += line
                pb_bar.next()  # noqa: B305
        return acc
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
    response.encoding = 'utf-8'
    return response.iter_content()
