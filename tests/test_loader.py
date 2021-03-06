# -*- coding:utf-8 -*-

"""Testing download."""

import os
from tempfile import TemporaryDirectory

import pytest

from page_loader import errors, loader, url


@pytest.mark.parametrize(  # noqa: WPS317, WPS211, WPS210
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
def test_loader(
    base_url, png_url, css_url,
    js_url, html, png, css, js,
    requests_mock, expected_html,
    expected_file_names,
):
    """Test download and save page."""
    with TemporaryDirectory() as tmpdirname:
        path_to_save = tmpdirname
        base_name = url.to_name(base_url)
        base_directory = url.to_name(base_url, directory=True)
        requests_mock.get(base_url, text=html)
        requests_mock.get(png_url, content=png)
        requests_mock.get(css_url, content=css)
        requests_mock.get(js_url, content=js)

        ouput = loader.download(base_url, path_to_save)
        assert len(os.listdir(tmpdirname)) == 2
        assert ouput == os.path.join(tmpdirname, base_name)

        local_resources = os.listdir(os.path.join(path_to_save, base_directory))
        assert set(local_resources) == expected_file_names

        with open(os.path.join(path_to_save, base_name)) as f:  # noqa: WPS111
            actually_html = f.read()

        assert actually_html == expected_html


def test_bad_loader(requests_mock):
    """Test bad download."""
    invalid_url = 'https://badsite.com'
    requests_mock.get(invalid_url, exc=errors.DownloadError)

    with TemporaryDirectory() as tmpdirname:

        with pytest.raises(Exception):  # noqa: PT011
            assert loader.download(invalid_url, tmpdirname)
        assert not os.listdir(tmpdirname)


@pytest.mark.parametrize('base_url', ['https://ru.hexlet.io/courses/{0}'])
@pytest.mark.parametrize('code', [404, 500])
def test_response_with_error(base_url, code, requests_mock):
    """Test bad responses."""
    url = base_url.format(code)  # noqa:WPS442
    requests_mock.get(url, status_code=code)

    with TemporaryDirectory() as tmpdirname:
        with pytest.raises(Exception):  # noqa: PT011
            assert loader.download(url, tmpdirname)
