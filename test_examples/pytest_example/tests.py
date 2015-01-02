# encoding: utf-8
"""
An example of testing a Flask app with py.test and Selenium with help of testliveserver.
"""

from os import path, environ
import sys
import six

from selenium import webdriver
import pytest
import liveandletdie

# Monkey patch the ssl module to disable SSL verification
# (see https://www.python.org/dev/peps/pep-0476/)
import ssl
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass


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
    'Django': liveandletdie.Django(
        abspath('sample_apps/django/example'),
        port=PORT
    ),
}

if six.PY2:
    APPS['Flask SSL'] = liveandletdie.Flask(
        abspath('sample_apps/flask/main.py'),
        port=PORT,
        ssl=True)
    APPS['GAE'] = liveandletdie.GAE(
        environ['VIRTUAL_ENV'] + '/bin/dev_appserver',
        abspath('sample_apps/gae'),
        port=PORT)

@pytest.fixture('module', APPS)
def app(request):
    app = APPS[request.param]
    app.name = request.param
    
    try:
        # Run the live server.
        app.live(kill_port=True)
    except Exception as e:
        # Skip test if not started.
        pytest.fail(e.message)
    
    request.addfinalizer(lambda: app.die())
    return app


@pytest.fixture('module')
def browser(request):
    liveandletdie.port_in_use(PORT, True)
    browser = webdriver.Firefox()
    browser.implicitly_wait(3)
    request.addfinalizer(lambda: browser.quit())
    return browser


def test_home(browser, app):
    """Andy visits a webpage and sees "Home"."""
    browser.get(app.check_url)
    page_text = browser.find_element_by_tag_name('body').text    
    assert 'Home {0}'.format(app.name) in page_text

