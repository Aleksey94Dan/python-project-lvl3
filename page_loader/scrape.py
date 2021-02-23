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
    except InvalidURL as err:
        raise InvalidURL('bls')
        # print(err)
        # print(err.args)
        # print(err.__cause__)
        # print(err.__context__)
    except MissingSchema as err:
        raise MissingSchema('ljl')
        # print(err)
        # print(err.args)
        # print(err.__cause__)
        # print(err.__context__)
    except InvalidSchema as err:
        raise InvalidSchema('asdfj')
        # print(err)
        # print(err.args)
        # print(err.__cause__)
        # print(err.__context__)
