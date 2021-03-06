# -*- coding:utf-8 -*-

"""Convert url for filename and directory."""

import os
import re
from typing import Optional
from urllib.parse import unquote, urljoin, urlparse

REPLACEMENT_SIGN = '-'
EXTENSIONS = ('.html', '.io', '', 'htm')
FILES = '_files'
ADAPTERS = ('http', 'https', '')
TEMPLATE = '{0}{1}'

PATTERN_FOR_STRIP = re.compile(r'(^\W+)|(\W+$)')
PATTERN_FOR_REPLACE = re.compile(r'\b(\W|_)+')
PATTERN_FOR_TAGS = re.compile(r'(link)|(script)|(img)')


def to_name(url: str, directory: bool = False) -> str:
    """Return the transformed name by pattern for base url."""
    url = unquote(url)
    parsed_url = urlparse(url)
    domain = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    domain = re.sub(PATTERN_FOR_STRIP, '', domain)
    url, extension = os.path.splitext(domain)
    name = re.sub(PATTERN_FOR_REPLACE, REPLACEMENT_SIGN, url.lower())
    if directory:
        return TEMPLATE.format(name, FILES)
    if extension in EXTENSIONS:
        return TEMPLATE.format(name, EXTENSIONS[0])
    return TEMPLATE.format(name, extension)


def to_full_url(base_url: str, local_url: str) -> Optional[str]:
    """Return the full url."""
    base_parsed = urlparse(base_url)
    local_parsed = urlparse(local_url)
    if local_parsed.scheme not in ADAPTERS:
        return None
    if base_parsed.netloc == local_parsed.netloc or not local_parsed.netloc:
        return urljoin(base_url, local_url)
    return None
