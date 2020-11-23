# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
from tempfile import TemporaryDirectory

import pytest
import requests_mock

from page_loader import loader

URL = 'https://ru.hexlet.io/courses'

with open('tests/fixture/site/index.html') as html:
    FORMS = html.read()

with open('tests/fixture/actual_urls') as urls:
    ACTUAL_URLS = urls.read().strip().splitlines()


@pytest.mark.parametrize('url', ACTUAL_URLS)
def test_get_name_from_url(url: str) -> None:
    """Test transformed name by pattern."""
    expected_pattern = re.compile(r'^[\w-]+\.html')
    assert re.fullmatch(expected_pattern, loader.get_name_from_url(url))


@pytest.mark.parametrize('url, message', [
    (
        'www.example.com/index.html',
        "'www.example.com/index.html' string has not scheme or netloc",
    ),
    (
        '/index',
        "'/index' string has not scheme or netloc",
    ),
    ('', 'Missing URL!'),
    (
        'www.example.com/{0}'.format('a' * loader.LIMITER_LENGTH_URL),
        'Your URL has passed the actual limit of 2000 characters.',
    ),
])
def test_get_name_from_url_exception(url: str, message: str) -> None:
    """Test exception transformed name by pattern."""
    with pytest.raises(ValueError, match=message):
        loader.get_name_from_url(url)


def test_scrape(requests_mock) -> None:  # noqa: WPS442
    """Test scrape."""
    requests_mock.get(URL, text=FORMS)
    assert FORMS == loader.scrape(URL)


def test_download() -> None:
    """Test os load page."""
    with TemporaryDirectory() as tmpdirname:
        name_file = loader.get_name_from_url(URL)
        path_to_file = os.path.join(tmpdirname, name_file)
        with requests_mock.Mocker() as mocker:
            mocker.get(URL, text=FORMS)
            loader.download(URL, directory=tmpdirname)
        assert os.path.exists(path_to_file)
