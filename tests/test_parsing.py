# -*- coding:utf-8 -*-

"""Testing text parsing."""


from page_loader import parsing


def test_get_urls(html, expected_urls):
    """Test getting urls."""
    prepared_html = parsing.prepare_html(html)
    tags = parsing.find_tags(prepared_html)
    actually_urls = set(parsing.get_urls(tags))

    assert expected_urls == actually_urls


def test_modify(html, expected_for_changed, changed_function):  # noqa: WPS210
    """Test modify html."""
    prepared_html = parsing.prepare_html(html)
    tags = parsing.find_tags(prepared_html)
    urls = parsing.get_urls(tags)
    for index, tag in enumerate(tags):
        tag.append(urls[index])

    actully_html = parsing.modify(prepared_html, tags, changed_function)

    assert expected_for_changed == actully_html
