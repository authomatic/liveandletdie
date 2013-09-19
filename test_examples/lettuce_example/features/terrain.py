from lettuce import *
from selenium import webdriver
import testliveserver

LIVESERVER_PATH = testliveserver.abspath(__file__, '../../../sample_apps/flask_sample/main.py')

@before.all
def setup_server_and_browser():
    print "starting server"
    world.server_process = testliveserver.start(LIVESERVER_PATH, '127.0.0.1:8001')
    
    print "starting browser"
    world.browser = webdriver.Chrome()
    world.browser.implicitly_wait(3)    
    
@after.all
def teardown_server_and_browser(total):
    print "terminating browser"
    world.browser.quit()
    
    print "stopping server"
    world.server_process.terminate()