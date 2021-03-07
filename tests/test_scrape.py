# -*- coding:utf-8 -*-

"""Testing scrape."""

import pytest

from page_loader import errors, scrape


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


@pytest.mark.parametrize(  # noqa: PT006
    (
        'url', 'message',
    ),
    [
        (
            'meduza.io', 'Your missed the "http/https" in url: {0}',
        ),
        (
            'https://medza.io', 'An error occurred connecting to {0}',
        ),
        (
            'httpd://meduza.io', 'You have the wrong scheme in url: {0}',
        ),
    ],
)
def test_wrong_request(url, message, requests_mock):
    """Test wrong requests."""
    requests_mock.get(
        url,
        exc=errors.DownloadError(message.format(url)),
    )
    with pytest.raises(Exception, match=message.format(url)):
        scrape.get_content(url)


@pytest.mark.parametrize(
    'code', [200, 300, 404, 500],
)
def test_bad_status_code(code, requests_mock):
    """Test response codes."""
    url = 'https://status_code/{0}'.format(code)
    requests_mock.get(url, status_code=code)
    with pytest.raises(Exception):  # noqa: PT011
        scrape.get(url)
