import testliveserver
import unittest
from selenium import webdriver

HOST = '127.0.0.1:8001'
HOME = 'http://{}/'.format(HOST)
LIVESERVER_PATH = testliveserver.abspath(__file__, '../../sample_apps/flask_sample/main.py')

class TestWebsite(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        try:
            # Run the live server.
            cls.process = testliveserver.start(LIVESERVER_PATH, HOST)
        except Exception as e:
            # Stop all tests if not started in timeout.
            raise unittest.SkipTest(e.message)
        
        # Start browser.
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(3)
    
    @classmethod
    def tearDownClass(cls):
        # Stop server.
        if hasattr(cls, 'process'):
            cls.process.terminate()
         
        # Stop browser.
        if hasattr(cls, 'browser'):
            cls.browser.quit()
    
    def test_visit_start_page(self):
        self.browser.get(HOME)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Home', page_text)


if __name__ == '__main__':
    unittest.main()