# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
from tempfile import TemporaryDirectory

import pytest
import requests_mock

from page_loader import loader

URL = 'https://aleksey94dan.github.io/'

with open('tests/fixture/site/index.html') as html:
    FORMS = html.read()

with open('tests/fixture/actual_base_urls') as base_urls:
    ACTUAL_BASE_URLS = base_urls.read().strip().splitlines()

with open('tests/fixture/actual_local_urls') as local_urls:
    ACTUAL_LOCAL_URLS = local_urls.read().strip().splitlines()


@pytest.mark.parametrize('url', ACTUAL_BASE_URLS)
def test_get_name_from_url(url: str) -> None:
    """Test transformed name by pattern for base url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.html')
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


@pytest.mark.parametrize('url', ACTUAL_LOCAL_URLS)
def test_get_name_from_local_resourse(url: str) -> None:
    """Test transformed name by pattern for local url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.(css|jpg|png|js)')
    print(loader.get_name_for_local_resource(url))
    assert re.fullmatch(expected_pattern, loader.get_name_for_local_resource(url))


def test_scrape(requests_mock) -> None:  # noqa: WPS442
    """Test scrape."""
    requests_mock.get(URL, text=FORMS)
    assert FORMS == loader.scrape(URL)


def test_download() -> None:  # noqa: WPS210
    """Test of load page."""
    with TemporaryDirectory() as tmpdirname:
        base_name = loader.get_name_from_url(URL)
        path_to_base_file = os.path.join(tmpdirname, base_name)
        path_to_base_directory = path_to_base_file.replace('.html', '_files')
        with requests_mock.Mocker() as mocker:
            mocker.get(URL, text=FORMS)
            loader.download(URL, directory=tmpdirname)
        assert os.path.isfile(path_to_base_file)
        assert os.path.isdir(path_to_base_directory)
