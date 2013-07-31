================
Test Live Server
================

**Test Live Server** is a very simple utility for running
a Flask development server for **BDD/functional** testing purposes.

I'm planning to add support for other frameworks in future.

Usage
-----

Add the **Test Live Server** capability to your Flask app by calling the
``testliveserver.flask.live_server(app)`` function just before the ``app.run()``.

.. code-block:: python
	
	from flask import Flask

	DEBUG = True
	SECRET_KEY = 'development key'
	USERNAME = 'admin'
	PASSWORD = 'default'

	app = Flask(__name__)
	app.config.from_object(__name__)

	@app.route('/')
	def home():
	    return 'Home'

	if __name__ == '__main__':
	    
	    # This does nothing unles you run this module with --testliveserver flag.
	    from testliveserver.flask import live_server
	    live_server(app)
	    
	    app.run()

In your test setup call the ``testliveserver.start(app_main, port_number)``
function which will run the Flask app with the ``--testliveserver`` flag.
The function returns the process of the running app
which you can terminate in the teardown.

.. code-block:: python
	
	import testliveserver
	import unittest
	from selenium import webdriver

	class TestWebsite(unittest.TestCase):
	    
	    @classmethod
	    def setUpClass(cls):
	    	# Start the server
	        try:
	            cls.process = testliveserver.start('main.py', 8001)
	        except Exception as e:
	            # Skip all tests if not started in timeout.
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
	    	self.browser.get('HTTP://127.0.0.1:8001')
	        page_text = self.browser.find_element_by_tag_name('body').text
	        self.assertIn('Home', page_text)


	if __name__ == '__main__':
	    unittest.main()