# -*- coding:utf-8 -*-

"""Testing text parsing."""


from page_loader import parsing


def test_get_urls(html, expected_urls):
    """Test getting urls."""
    prepared_html = parsing.prepare_html(html)
    tags = parsing.find_tags(prepared_html)
    actually_urls = parsing.get_urls(tags)

    actually_urls.sort()
    expected_urls.sort()

    assert expected_urls == actually_urls


def test_modify(html, expected_for_changed, changed_function):
    """Test modify html."""
    prepared_html = parsing.prepare_html(html)
    tags = parsing.find_tags(prepared_html)
    actully_html = parsing.modify(prepared_html, tags, changed_function)

    assert expected_for_changed == actully_html
