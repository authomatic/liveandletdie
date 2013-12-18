from os import path

import liveandletdie
import unittest
from selenium import webdriver


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


PORT = 8001


class Base(unittest.TestCase):
    EXPECTED_TEXT = None
    APP = None
    
    @classmethod
    def setUpClass(cls):
        try:
            # Run the live server.
            cls.APP.start(kill=True)
        except Exception as e:
            # Skip test if not started.
            raise unittest.SkipTest(e.message)
        
        # Start browser.
        cls.browser = webdriver.PhantomJS()
        cls.browser.implicitly_wait(3)
    
    @classmethod
    def tearDownClass(cls):
        # Stop server.
        if hasattr(cls, 'process'):
            cls.APP.stop()
         
        # Stop browser.
        if hasattr(cls, 'browser'):
            cls.browser.quit()
    
    def test_visit_start_page(self):
        self.browser.get(self.APP.url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(self.EXPECTED_TEXT, page_text)


class TestFlask(Base):
    EXPECTED_TEXT = 'Home Flask'
    APP = liveandletdie.Flask(abspath('sample_apps/flask/main.py'), port=PORT)


class TestPyramid(Base):
    EXPECTED_TEXT = 'Home Pyramid'
    APP = liveandletdie.WsgirefSimpleServer(abspath('sample_apps/pyramid/main.py'), port=PORT)


class TestDjango(Base):
    EXPECTED_TEXT = 'Home Django'
    APP = liveandletdie.Django(abspath('sample_apps/django/example'), port=PORT)


class TestGAE(Base):
    EXPECTED_TEXT = 'Home GAE'
    APP = liveandletdie.GAE(abspath('venv/bin/google_appengine/dev_appserver.py'),
                  abspath('sample_apps/gae'), port=PORT)


if __name__ == '__main__':
    unittest.main()