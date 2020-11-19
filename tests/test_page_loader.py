# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import re
import pytest

ACTUAL_URL = 'path_to_file'

def test_get_name_from_url():

    with open(ACTUAL_URL) as url:
        actual = url.read().strip().split()

    actuals = map(get_name_from_url, actual)
    expected = re.compile(r'^[\w-]+\.html')
    
    for actual in actuals:
        assert actual == expected, "URL does not match pattern"
    
