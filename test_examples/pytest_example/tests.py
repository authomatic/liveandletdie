# encoding: utf-8
"""
An example of testing a Flask app with py.test and Selenium with help of testliveserver.
"""

from os import path

from selenium import webdriver
import pytest
import testliveserver as tls


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


APPS = {
    'Pyramid': tls.WsgirefSimpleServer(
        abspath('sample_apps/pyramid/main.py'),
        port=5000
    ),
    'Flask': tls.Flask(
        abspath('sample_apps/flask/main.py'),
        port=5000
    ),
    'GAE': tls.GAE(
        abspath('venv/bin/google_appengine/dev_appserver.py'),
        abspath('sample_apps/gae'),
        port=8080
    ),
}


@pytest.fixture('module', APPS)
def app(request):
    app = APPS[request.param]
    
    try:
        # Run the live server.
        app.start(kill=True)
    except Exception as e:
        # Skip test if not started.
        pytest.fail(e.message)
    
    request.addfinalizer(lambda: app.stop())
    return app


@pytest.fixture('module')
def browser(request):
    browser = webdriver.Chrome()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


def test_home(browser, app):
    """Andy visits a webpage and sees "Home"."""
    
    browser.get(app.url)
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Home' in page_text