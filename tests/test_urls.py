# -*- coding:utf-8 -*-

"""Testing file and directory names."""
import pytest

from page_loader import url


@pytest.mark.parametrize(
    (
        'actually_url', 'expected_url',
    ),
    [
        ('http://www.example.com/index.html/', 'www-example-com-index.html'),
        ('http://www.EXAMPLE.com/index.html/', 'www-example-com-index.html'),
        ('https://ru.hexlet.io/courses/', 'ru-hexlet-io-courses.html'),
        (
            'https://en.wikipedia.org/wiki/URL/',
            'en-wikipedia-org-wiki-url.html',
        ),
        ('https://aliexpress.ru/home.htm/', 'aliexpress-ru-home.htm'),
        (
            'https://www.windy.com/ru/-%D0%A0%D0%9C2-5-pm2p5?cams,'
            'pm2p5,55.332,86.054,11a',
            'www-windy-com-ru-pm2-5-pm2p5.html',
        ),
        (
            'https://campaign.aliexpress.com/wow/gcp/ae/channel/ae/accelerate/'
            'tupr?spm=a2g0o.home.15027.1.17ba5c98ckbHwJ&wh_pid=ae/mega/ae/2020'
            '_super_friday/shoes&wh_weex=true&_immersiveMode=true&wx_navbar_hi'
            'dden=true&wx_navbar_transparent=true&ignoreNavigationBar=true&wx_'
            'statusbar_hidden=true&gps-id=300000000564511&productIds='
            '400113214004ca',
            'mpaign-aliexpress-com-wow-gcp-ae-channel-ae-accelerate-tupr.html',
        ),
        ('/imagenes/logo-akus.jpg/', 'imagenes-logo-akus.jpg'),
        ('/en-US/docs/style.css/', 'en-us-docs-style.css'),
        ('/en-US/docs/Learn.png/', 'en-us-docs-learn.png'),
        ('/en-US/docs/', 'en-us-docs.html'),
    ],
)
def test_to_name(actually_url, expected_url):
    """Test transformed name."""
    assert expected_url == url.to_name(expected_url)


@pytest.mark.parametrize(
    (
        'actually_url', 'expected_name',
    ),
    [
        ('http://www.EXAMPLE.com/index.html/', 'www-example-com-index_files'),
        ('https://ru.hexlet.io/courses/', 'ru-hexlet-io-courses_files'),
        ('https://ru.hexlet.io/', 'ru-hexlet_files'),
        (
            'https://en.wikipedia.org/wiki/URL',
            'en-wikipedia-org-wiki-url_files',
        ),
    ],
)
def test_to_dir_name(actually_url, expected_name):
    """Test name for path to directory."""
    assert expected_name == url.to_name(actually_url, directory=True)


@pytest.mark.parametrize(
    (
        'base_url', 'local_url', 'expected_url',
    ),
    [
        (
            'https://ru.hexlet.io/courses',
            'https://ru.hexlet.io/packs/js/runtime.js',
            'https://ru.hexlet.io/packs/js/runtime.js',
        ),
        (
            'https://ru.hexlet.io/courses',
            '/assets/application.css',
            'https://ru.hexlet.io/assets/application.css',
        ),
        (
            'https://ru.hexlet.io/courses',
            '/courses',
            'https://ru.hexlet.io/courses',
        ),
        (
            'https://ru.hexlet.io/courses',
            '/assets/professions/nodejs.png',
            'https://ru.hexlet.io/assets/professions/nodejs.png',
        ),
        (
            'https://ru.hexlet.io/courses',
            'https://cdn2.hexlet.io/assets/menu.css',
            None,
        ),
        (
            'https://ru.hexlet.io/courses',
            'https://js.stripe.com/v3/',
            None,
        ),
        (
            'https://meduza.io/',
            'data:image',
            None,
        ),
    ],
)
def test_to_full_url(base_url, local_url, expected_url):
    """Test name for full url."""
    assert expected_url == url.to_full_url(base_url, local_url)
