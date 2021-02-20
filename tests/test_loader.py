# -*- coding:utf-8 -*-

"""Testing download."""

import os
from tempfile import TemporaryDirectory

import pytest

from page_loader import loader, url


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
    expected_file_name,
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

        loader.download(base_url, path_to_save)
        local_resource = os.listdir(os.path.join(path_to_save, base_directory))
        local_resource.sort()
        expected_file_name.sort()

        with open(os.path.join(path_to_save, base_name)) as f:  # noqa: WPS111
            actually_html = f.read()

        assert actually_html == expected_html
        assert local_resource == expected_file_name