# -*- coding:utf-8 -*-

"""The module sends HTTP requests to the content."""

from typing import Union

import requests
from requests.exceptions import (
    MissingSchema,
    InvalidURL,
    InvalidSchema,
)


def get_content(url: str) -> Union[str, bytes]:
    """Pull page content."""
    try:
        response = requests.get(url)
        return response.text if response.encoding else response.content
    except InvalidURL as err1:
        raise InvalidURL()
    except MissingSchema as err2:
        raise MissingSchema()
    except InvalidSchema as err3:
        raise InvalidSchema()