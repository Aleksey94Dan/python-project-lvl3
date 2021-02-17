# -*- coding:utf-8 -*-

"""The module sends HTTP requests to the content."""

from typing import Union

import requests


def get_content(url: str) -> Union[str, bytes]:
    """Pull page content."""
    response = requests.get(url)
    return response.text if response.encoding else response.content
