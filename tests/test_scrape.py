# -*- coding:utf-8 -*-

"""Testing scrape."""

import pytest

from page_loader import scrape


@pytest.mark.parametrize(  # noqa: WPS317, WPS211
    (
        'base_url', 'png_url', 'css_url', 'js_url',
    ),
    [
        (
            'https://ru.hexlet.io/courses',
            'https://ru.hexlet.io/assets/professions/nodejs.png',
            'https://ru.hexlet.io/assets/application.css',
            'https://ru.hexlet.io/packs/js/runtime.js',
        ),
    ],
)
def test_get_content(
    base_url, png_url, css_url,
    js_url, html, png, css, js,
    requests_mock,
):
    """Test requests."""
    requests_mock.get(base_url, text=html)
    requests_mock.get(png_url, content=png)
    requests_mock.get(css_url, content=css)
    requests_mock.get(js_url, content=js)

    assert html == scrape.get_content(base_url)
    assert png == scrape.get_content(png_url)
    assert css == scrape.get_content(css_url)
    assert js == scrape.get_content(js_url)
