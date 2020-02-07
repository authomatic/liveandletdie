# encoding: utf-8
"""
An example of testing a Flask app with py.test and Selenium with help of testliveserver.
"""

from os import path, environ
import sys

import liveandletdie
import pytest
import requests


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


PORT = 8001
APPS = {
    'Pyramid': liveandletdie.WsgirefSimpleServer(
        abspath('sample_apps/pyramid/main.py'),
        port=PORT
    ),
    'Pyramid SSL': liveandletdie.WsgirefSimpleServer(
        abspath('sample_apps/pyramid/main.py'),
        port=PORT,
        ssl=True
    ),
    'Flask': liveandletdie.Flask(
        abspath('sample_apps/flask/main.py'),
        port=PORT
    ),
    'Flask SSL': liveandletdie.Flask(
        abspath('sample_apps/flask/main.py'),
        port=PORT,
        ssl=True
    ),
    'Django': liveandletdie.Django(
        abspath('sample_apps/django/example'),
        port=PORT
    ),
}


if sys.version_info[0] is 2 and sys.version_info[1] is 7:
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


def test_home(app):
    """Andy visits a webpage and sees "Home"."""
    page_text = requests.get(app.check_url, verify=False).\
        content.decode('utf-8')

    assert 'Home {0}'.format(app.name) in page_text
