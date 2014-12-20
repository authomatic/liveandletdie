from os import path, environ
import six

import liveandletdie
from selenium import webdriver

try:
    import unittest2 as unittest
except ImportError:
    import unittest


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


PORT = 8001


def test_decorator(cls):
    @classmethod
    def setUpClass(cls):
        try:
            # Run the live server.
            cls.app.live(kill_port=True)
        except Exception as e:
            # Skip test if not started.
            raise unittest.SkipTest(e.message)
        
        # Start browser.
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(3)
    
    @classmethod
    def tearDownClass(cls):
        # Stop server.
        cls.app.die()
         
        # Stop browser.
        if hasattr(cls, 'browser'):
            cls.browser.quit()
    
    def test_visit_start_page(self):
        self.browser.get(self.app.check_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(self.EXPECTED_TEXT, page_text)

    cls.setUpClass = setUpClass
    cls.tearDownClass = tearDownClass
    cls.test_visit_start_page = test_visit_start_page
    return cls


@test_decorator
class TestFlask(unittest.TestCase):
    EXPECTED_TEXT = 'Home Flask'
    app = liveandletdie.Flask(abspath('sample_apps/flask/main.py'), port=PORT)


@unittest.skipIf(six.PY3, "Werkzeug has a bug with Py3k and SSL")
@test_decorator
class TestFlaskSSL(unittest.TestCase):
    EXPECTED_TEXT = 'Home Flask SSL'
    app = liveandletdie.Flask(abspath('sample_apps/flask/main.py'), port=PORT,
                              ssl=True)


@test_decorator
class TestPyramid(unittest.TestCase):
    EXPECTED_TEXT = 'Home Pyramid'
    app = liveandletdie.WsgirefSimpleServer(abspath('sample_apps/pyramid/main.py'), port=PORT)


@test_decorator
class TestDjango(unittest.TestCase):
    EXPECTED_TEXT = 'Home Django'
    app = liveandletdie.Django(abspath('sample_apps/django/example'), port=PORT)


@unittest.skipIf(six.PY3, "GAE not implemented for Py3k")
@test_decorator
class TestGAE(unittest.TestCase):
    EXPECTED_TEXT = 'Home GAE'
    app = liveandletdie.GAE(environ['VIRTUAL_ENV'] + '/bin/dev_appserver',
                  abspath('sample_apps/gae'), port=PORT)


if __name__ == '__main__':
    unittest.main()
