# -*- coding:utf-8 -*-

"""Prepare fixtures."""

from pathlib import Path
from typing import Union

import pytest

BASE_URL = 'https://ru.hexlet.io/courses'
PNG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'

BASE_HTML = 'tests/fixture/site/index.html'
EXPECTED_HTML = 'tests/fixture/site/expected/expected.html'
PNG = 'tests/fixture/site/assets/professions/nodejs.png'
CSS = 'tests/fixture/site/assets/application.css'
JS = 'tests/fixture/site/packs/js/runtime.js'


def _get_file(path_to_file: Path, mode: str = 'r') -> Union[str, bytes]:
    with open(path_to_file, mode) as f:  # noqa: WPS111
        return f.read()


@pytest.fixture()
def html():
    """Return html file."""
    return _get_file(BASE_HTML)


@pytest.fixture()
def expected_html():
    """Return expected html file."""
    return _get_file(EXPECTED_HTML)


@pytest.fixture()
def png():
    """Return png file."""
    return _get_file(PNG, 'br')


@pytest.fixture()
def css():
    """Return css file."""
    return _get_file(CSS, 'br')


@pytest.fixture()
def js():
    """Return js file."""
    return _get_file(JS, 'br')


@pytest.fixture()
def expected_urls():
    """Return urls for paring case."""
    return [
        'https://cdn2.hexlet.io/assets/menu.css',
        '/assets/application.css',
        '/courses',
        '/assets/professions/nodejs.png',
        'https://js.stripe.com/v3/',
        'https://ru.hexlet.io/packs/js/runtime.js',
    ]


@pytest.fixture()
def changed_urls():
    """Return attributes along with changed url."""
    return [
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css',
        'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html',
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions'
        '-nodejs.png',
        'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js',
    ]
