# -*- coding:utf-8 -*-

"""The module transforms the url and loads the html."""


from urllib.parse import urlparse, unquote
import re
import os


ATRIBUTES = ('scheme', 'netloc')
REPLACEMENT_SIGN = '-'
EXTENSION = '.html'
BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'









@make_short_name
def get_name_from_url(url: str) -> str:
    length_url = len(url)
    if not url:
        raise ValueError('Missing URL!')

    if length_url > 2000:
        raise ValueError(
    'Your URL has passed the actual limit of 2000 characters.'
    )

    url = unquote(url)
    parsed_url = urlparse(url)

    if not all((getattr(parsed_url, atribute) for atribute in ATRIBUTES)):
        raise ValueError("'{}' string has not scheme or netloc".format(url))

    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    pattern = re.compile(r'\W|_')
    name = re.sub(pattern, REPLACEMENT_SIGN, domain)
    return '{0}{1}'.format(name, EXTENSION)

