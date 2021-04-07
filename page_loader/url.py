# -*- coding:utf-8 -*-

"""Convert url for filename and directory."""

import os
import re
from typing import Optional
from urllib.parse import unquote, urljoin, urlparse

REPLACEMENT_SIGN = '-'
EXTENSIONS = ('.html', '', 'htm')
FILES = '_files'
SCHEMES = ('http', 'https', '')

PATTERN_FOR_STRIP = re.compile(r'(^\W+)|(\W+$)')
PATTERN_FOR_REPLACE = re.compile(r'\b(\W|_)+')
PATTERN_FOR_TAGS = re.compile(r'(link)|(script)|(img)')


def to_name(url: str, directory: bool = False) -> str:  # noqa: WPS210
    """Return the transformed name by pattern for base url."""
    parsed_url = urlparse(unquote(url))
    domain = parsed_url.netloc + parsed_url.path
    domain = re.sub(PATTERN_FOR_STRIP, '', domain)
    url, extension = os.path.splitext(domain)
    name = re.sub(PATTERN_FOR_REPLACE, REPLACEMENT_SIGN, url.lower())
    if directory:
        suffix = FILES
    elif extension in EXTENSIONS:
        suffix = EXTENSIONS[0]
    else:
        suffix = extension
    return name + suffix


def to_full_url(base_url: str, local_url: str) -> Optional[str]:
    """Return the full url."""
    base_parsed = urlparse(base_url)
    local_parsed = urlparse(local_url)
    if local_parsed.scheme not in SCHEMES:
        return None
    if base_parsed.netloc == local_parsed.netloc or not local_parsed.netloc:
        return urljoin(base_url, local_url)
    return None
