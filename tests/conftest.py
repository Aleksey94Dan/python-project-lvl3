from pytest_localserver.http import WSGIServer

import pytest
import requests


def scrape(url):
    html = requests.get(url).text
    return html


def simple_app(environ, start_response):
    """Simplest possible WSGI application"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n'.encode('utf-8')]


@pytest.fixture
def testserver(request):
    """Defines the testserver funcarg"""
    server = WSGIServer(application=simple_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


def test_retrieve_some_content(testserver):
    assert scrape(testserver.url) == 'Hello world!\n'
