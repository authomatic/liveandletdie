from __future__ import print_function
from lettuce import *

import sample_apps


@before.all
def setup_browser():
    print("starting browser")
    world.browser = sample_apps.get_browser()
    world.browser.implicitly_wait(3)    
     
@after.all
def teardown_browser_and_server(total):
    print("terminating browser")
    world.browser.quit()
