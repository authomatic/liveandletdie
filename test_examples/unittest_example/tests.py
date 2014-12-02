from os import path

import liveandletdie
from selenium import webdriver

try:
    import unittest2 as unittest
except ImportError:
    import unittest


def abspath(pth):
    return path.join(path.dirname(__file__), '../..', pth)


PORT = 8001


class Base(unittest.TestCase):
    EXPECTED_TEXT = None
    app = None
    
    @classmethod
    def setUpClass(cls):
        try:
            # Run the live server.
            cls.app.live(kill=True)
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


class TestFlask(Base):
    EXPECTED_TEXT = 'Home Flask'
    app = liveandletdie.Flask(abspath('sample_apps/flask/main.py'), port=PORT)


class TestFlaskSSL(Base):
    EXPECTED_TEXT = 'Home Flask SSL'
    app = liveandletdie.Flask(abspath('sample_apps/flask/main.py'), port=PORT,
                              ssl=True)


class TestPyramid(Base):
    EXPECTED_TEXT = 'Home Pyramid'
    app = liveandletdie.WsgirefSimpleServer(abspath('sample_apps/pyramid/main.py'), port=PORT)


class TestDjango(Base):
    EXPECTED_TEXT = 'Home Django'
    app = liveandletdie.Django(abspath('sample_apps/django/example'), port=PORT)


class TestGAE(Base):
    EXPECTED_TEXT = 'Home GAE'
    app = liveandletdie.GAE(abspath('venv/bin/dev_appserver'),
                  abspath('sample_apps/gae'), port=PORT, kill_orphans=True)


if __name__ == '__main__':
    unittest.main()