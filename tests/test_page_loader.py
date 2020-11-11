# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import os
import re
import tempfile

import pytest

from page_loader import loader

URL = r"https://hexlet.io/courses"

@pytest.mark.parametrize("url", [URL])
def test_name(url):
    """Testing a filename against a pattern."""
    pattern = r'([a-zA-Z0-9-]+)((\.html)|(_files))'
    name_file = loader.get_name(url)
    name_directory = loader.get_name(url)
    assert re.fullmatch(pattern, name_file)


@pytest.mark.parametrize("url", [URL])
def test_load_page(url):
    """Test of page load"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        name_file = loader.get_name(url)
        path_to_file = os.path.join(tmpdirname, name_file)
        loader.load(url, directory=tmpdirname)
        assert os.path.isfile(path_to_file)

