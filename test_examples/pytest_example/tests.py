# encoding: utf-8
"""
An example of testing a Flask app with py.test and Selenium with help of testliveserver.
"""

from os import path
import sys

print sys.path

from selenium import webdriver
import pytest
import liveandletdie


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


PORT = 8001


APPS = {
    'Pyramid': liveandletdie.WsgirefSimpleServer(
        abspath('sample_apps/pyramid/main.py'),
        port=PORT
    ),
    'Flask': liveandletdie.Flask(
        abspath('sample_apps/flask/main.py'),
        port=PORT
    ),
    'GAE': liveandletdie.GAE(
        abspath('venv/bin/google_appengine/dev_appserver.py'),
        abspath('sample_apps/gae'),
        port=PORT
    ),
    'Django': liveandletdie.Django(
        abspath('sample_apps/django/example'),
        port=PORT
    ),
}


@pytest.fixture('module', APPS)
def app(request):
    app = APPS[request.param]
    app.name = request.param
    
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
    
    liveandletdie.port_in_use(PORT, True)
    
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(3)
    
    request.addfinalizer(lambda: browser.quit())
    return browser


def test_home(browser, app):
    """Andy visits a webpage and sees "Home"."""
        
    browser.get(app.url)    
    page_text = browser.find_element_by_tag_name('body').text    
    assert 'Home {}'.format(app.name) in page_text

