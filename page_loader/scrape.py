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


def get_content(url: str) -> Union[str, bytes]:
    """Pull page content."""
    try:
        response = requests.get(url)
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
    return response.text if response.encoding else response.content
