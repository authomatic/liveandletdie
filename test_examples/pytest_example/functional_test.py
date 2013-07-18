# encoding: utf-8
"""
An example of testing a Flask app with py.test and Selenium with help of testliveserver.
"""

from selenium import webdriver
import pytest
import testliveserver


HOST = '127.0.0.1:8001'
HOME = 'http://{}/'.format(HOST)
LIVESERVER_PATH = testliveserver.rp(__file__, '../../sample_apps/flask_sample/main.py')


class TestLogin(object):
    """
    Tests interaction of a user with a website.
    """
    
    def setup_class(self):
        try:
            # Run the live server.
            self.process = testliveserver.start(LIVESERVER_PATH, HOST)
        except Exception as e:
            # Stop all tests if not started.
            pytest.exit(format(e.message))
        
        # Start the browser.
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
                
        
    def teardown_class(self):
        # Stop the live server.
        if hasattr(self, 'process'):
            self.process.terminate()
         
        # Stop the browser.
        if hasattr(self, 'browser'):
            self.browser.quit()    
    
    
    def test_visit_start_page(self):
        """Andy visits a webpage and sees the "Home" text."""
        
        self.browser.get(HOME)
        page_text = self.browser.find_element_by_tag_name('body').text
        assert 'Home' in page_text