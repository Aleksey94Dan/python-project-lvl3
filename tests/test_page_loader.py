# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import re
import pytest

from page_loader import loader

with open('tests/fixture/actual_urls') as urls:
    ACTUAL_URLS = urls.read().strip().splitlines()



@pytest.mark.parametrize('url', ACTUAL_URLS)
def test_get_name_from_url(url):
    expected_pattern = re.compile(r'^[\w-]+\.html')
    assert re.fullmatch(expected_pattern, loader.get_name_from_url(url))


@pytest.mark.parametrize('url, message', [
    ('www.example.com/index.html', "'www.example.com/index.html' string has not scheme or netloc"),
    ('/index', "'/index' string has not scheme or netloc"),
    ('', "Missing URL!"),
    ('www.example.com/' + '/a'*2000, 'Your URL has passed the actual limit of 2000 characters.')
])
def test_get_name_from_url_exception(url, message):
    with pytest.raises(ValueError, match=message):
        loader.get_name_from_url(url)
