# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
from tempfile import TemporaryDirectory

import pytest

from page_loader import loader



with open('tests/fixture/actual_base_urls') as base_urls:
    ACTUAL_BASE_URLS = base_urls.read().strip().splitlines()

@pytest.mark.parametrize('url', ACTUAL_BASE_URLS)
def test_get_name_from_url(url: str) -> None:
    """Test transformed name by pattern for base url."""
    expected_pattern = re.compile(r'^\w+\-?(\w+\-?)+\.\w+$')

    assert re.fullmatch(expected_pattern, loader.get_name_from_url(url))


# @pytest.mark.parametrize(  # noqa: WPS317
#     ('url', 'message'),
#     [
#         (
#             'www.example.com/index.html',
#             "'www.example.com/index.html' string has not scheme or netloc",
#         ),
#         (
#             '/index',
#             "'/index' string has not scheme or netloc",
#         ),
#         ('', 'Missing URL!'),
#         (
#             'www.example.com/{0}'.format('a' * loader.LIMITER_LENGTH_URL),
#             'Your URL has passed the actual limit of 2000 characters.',
#         ),
#     ],
# )
# def test_get_name_from_url_exception(url: str, message: str) -> None:
#     """Test exception transformed name by pattern."""
#     with pytest.raises(ValueError, match=message):
#         loader.get_name_from_url(url)



# def test_scrape_text(requests_mock) -> None:  # noqa: WPS442
#     """Test scrape text and content."""
#     requests_mock.get(BASE_URL, text=FORMS)
#     requests_mock.get(CONTENT_URL, content=CONTENT)

#     assert FORMS == loader.scrape(BASE_URL)
#     assert CONTENT == loader.scrape(CONTENT_URL)


# def test_download(requests_mock) -> None:  # noqa: WPS210
#     """Test of load page."""
#     with TemporaryDirectory() as tmpdirname:
#         base_name = loader.get_name_from_url(BASE_URL)
#         path_to_base_file = os.path.join(tmpdirname, base_name)
#         path_to_base_directory = path_to_base_file.replace('.html', '_files')
#         requests_mock.get(BASE_URL, text=FORMS)
#         requests_mock.get(CONTENT_URL, content=CONTENT)
#         loader.download(BASE_URL, directory=tmpdirname)

#         with open(path_to_base_file) as html:
#             actual_html = html.read()
#         assert actual_html == EXPECTED_FORMS
#         assert os.path.isfile(path_to_base_file)
#         assert os.path.isdir(path_to_base_directory)
#         assert NAME_IMAGE in os.listdir(path_to_base_directory)
