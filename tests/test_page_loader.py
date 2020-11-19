# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import re
import pytest

ACTUAL_URL = 'path_to_file'
EXPECTED_URL = 'path_to_file'


def test_get_name_from_url():

    with open(ACTUAL_URL) as url:
        actual = url.read().strip().split()

    with open(EXPECTED_URL) as url:
        expected = url.read().strip().split()

    actual = sorted(map(get_name_from_url, actual))
    expected = sorted(expected)

    assert actual == expected
