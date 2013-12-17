from lettuce import *
from selenium import webdriver
 
@before.all
def setup_browser():
    print "starting browser"
    world.browser = webdriver.PhantomJS()
    world.browser.implicitly_wait(3)    
     
@after.all
def teardown_browser_and_server(total):
    print "terminating browser"
    world.browser.quit()