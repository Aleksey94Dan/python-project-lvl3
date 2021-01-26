# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
from tempfile import TemporaryDirectory

import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup

from page_loader import loader, logging_app

BASE_URL = 'https://ru.hexlet.io/courses'
PNG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'

MODE = 'rb'

with open('tests/fixture/actual_base_urls') as base_urls:
    ACTUAL_BASE_URLS = base_urls.read().strip().splitlines()

with open('tests/fixture/site/index.html') as html:
    FORMS = html.read()

with open('tests/fixture/site/expected/expected.html') as forms:
    EXPECTED_FORMS = forms.read()

with open('tests/fixture/site/assets/professions/nodejs.png', MODE) as img:
    CONTENT = img.read()

with open('tests/fixture/site/assets/professions/nodejs.png', MODE) as css:
    CONTENT_CSS = css.read()

with open('tests/fixture/site/packs/js/runtime.js', MODE) as js:
    CONTENT_JS = js.read()

logger = logging_app.logger


@pytest.mark.parametrize('url', ACTUAL_BASE_URLS)
def test_get_name_from_url(url):
    """Test transformed name by pattern for base url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.\w+$')

    assert re.fullmatch(expected_pattern, loader.get_name_from_url(url))


@pytest.mark.parametrize(  # noqa: WPS317
    ('url', 'message', 'type_of_raise'),
    [
        ('', 'Missing URL!', ValueError),
        (123, "Incorrectly entered URL! Expected 'str'.", TypeError),
        (True, "Incorrectly entered URL! Expected 'str'.", TypeError),
        (
            'www.example.com/{0}'.format('a' * loader.LIMITER_LENGTH_URL),
            'Your URL has passed the actual limit of 2000 characters.',
            ValueError,
        ),
    ],
)
def test_raise_url(url, message, type_of_raise):
    """Test exception transformed name by pattern."""
    with pytest.raises(type_of_raise, match=message):
        loader.raise_url(url)


def test_scrape_text(requests_mock):  # noqa: WPS442
    """Test scrape text and content."""
    requests_mock.get(BASE_URL, text=FORMS)
    requests_mock.get(PNG_URL, content=CONTENT)

    assert FORMS == loader.scrape(BASE_URL)
    assert CONTENT == loader.scrape(PNG_URL)


def test_write_data():
    """Test write data."""
    with TemporaryDirectory() as tmpdirname:
        name = 'image.png'
        path_to_file = os.path.join(tmpdirname, name)
        loader.write_data(CONTENT, path_to_file)
        with open(path_to_file, 'rb') as f:  # noqa: WPS111
            actual_content = f.read()
        assert CONTENT == actual_content


def test_download(requests_mock):  # noqa: WPS210, WPS442
    """Test of load page."""
    with TemporaryDirectory() as tmpdirname:
        base_name = loader.get_name_from_url(BASE_URL)
        path_to_base_file = os.path.join(tmpdirname, base_name)
        path_to_base_directory = os.path.join(
            tmpdirname, path_to_base_file.replace('.html', '_files'),
        )
        requests_mock.get(BASE_URL, text=FORMS)
        requests_mock.get(PNG_URL, content=CONTENT)
        requests_mock.get(CSS_URL, content=CONTENT_CSS)
        requests_mock.get(JS_URL, content=CONTENT_JS)
        loader.download(BASE_URL, tmpdirname)

        with open(path_to_base_file) as f:  # noqa: WPS111
            actual_html = f.read()
        soup = BeautifulSoup(EXPECTED_FORMS, 'lxml')
        expected_html = soup.prettify(formatter='html5')
        assert actual_html == expected_html
        assert os.path.isfile(path_to_base_file)
        assert os.path.exists(path_to_base_directory)


def test_requests_not_found():
    """Test for 404 Non found."""
    adapter = requests_mock.Adapter()
    adapter.register_uri(
        'GET', 'mock://test.com/6', exc=requests.exceptions.InvalidSchema,
    )
    with pytest.raises(requests.exceptions.InvalidSchema):
        loader.scrape('mock://test.com/6')
