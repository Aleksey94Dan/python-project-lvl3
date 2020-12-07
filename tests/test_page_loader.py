# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
from tempfile import TemporaryDirectory

import pytest
import requests_mock

from page_loader import loader

BASE_URL = 'https://aleksey94dan.github.io/'
CONTENT_URL = 'https://aleksey94dan.github.io/'


with open('tests/fixture/site/index.html') as html:
    FORMS = html.read()

with open('tests/fixture/site/expected/expected.html') as expected_html:
    EXPECTED_FORMS = expected_html.read()

with open('tests/fixture/site/assets/professions/nodejs.png', 'rb') as image:
    CONTENT = image.read()

with open('tests/fixture/actual_base_urls') as base_urls:
    ACTUAL_BASE_URLS = base_urls.read().strip().splitlines()

with open('tests/fixture/actual_local_urls') as local_urls:
    ACTUAL_LOCAL_URLS = local_urls.read().strip().splitlines()


@pytest.mark.parametrize('url', ACTUAL_BASE_URLS)
def test_get_name_from_url(url: str) -> None:
    """Test transformed name by pattern for base url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.html')
    assert re.fullmatch(expected_pattern, loader.get_name_from_url(url))


@pytest.mark.parametrize(  # noqa: WPS317
    ('url', 'message'),
    [
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
    ],
)
def test_get_name_from_url_exception(url: str, message: str) -> None:
    """Test exception transformed name by pattern."""
    with pytest.raises(ValueError, match=message):
        loader.get_name_from_url(url)


@pytest.mark.parametrize('url', ACTUAL_LOCAL_URLS)
def test_get_name_from_local_resourse(url: str) -> None:
    """Test transformed name by pattern for local url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.(css|jpg|png|js)')
    assert re.fullmatch(
        expected_pattern, loader.get_name_for_local_resource(url),
    )


@pytest.mark.parametrize(  # noqa: WPS317
    ('forms', 'image'),
    [
        (FORMS, None),
        (None, CONTENT),
    ],
)
def test_scrape_text(requests_mock, forms, image) -> None:  # noqa: WPS442
    """Test scrape text and content."""
    requests_mock.get(BASE_URL, text=forms, content=image)
    if forms:
        assert FORMS == loader.scrape(BASE_URL)
    if image:
        assert CONTENT == loader.scrape(CONTENT_URL)


def test_download() -> None:  # noqa: WPS210
    """Test of load page."""
    with TemporaryDirectory() as tmpdirname:
        base_name = loader.get_name_from_url(BASE_URL)
        path_to_base_file = os.path.join(tmpdirname, base_name)
        path_to_base_directory = path_to_base_file.replace('.html', '_files')
        with requests_mock.Mocker() as mocker:
            mocker.get(BASE_URL, text=FORMS)
            loader.download(BASE_URL, directory=tmpdirname)
            with open(path_to_base_file) as base_file:
                actual_html = base_file.read()
        assert os.path.isfile(path_to_base_file)
        assert os.path.isdir(path_to_base_directory)
        assert EXPECTED_FORMS.encode('utf-8') == actual_html.encode('utf-8')
