# -*- coding: utf-8 -*-
import os
import six

from lettuce import step, world
from selenium import webdriver
from functools import wraps

import liveandletdie

class SkipOnPy3k:

    def __init__(self):
        self.skip_test = False

    def call(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.skip_test:
                return func(*args, **kwargs)
        return wrapper

    def init(self, func):
        @wraps(func)
        def wrapper(step, framework, path):
            self.skip_test = framework == six.u('GAE') and not six.PY2
            print(framework, six.PY2, self.skip_test)
            if not self.skip_test:
                return func(step, framework, path)
        return wrapper

skip_on_py3k = SkipOnPy3k()

@step('Given a web application based on (\w+) located at ([\w/.]+)')
@skip_on_py3k.init
def given_a_web_application_based_on_framework_located_at_path(step, framework, path):

    world.AppClass = getattr(liveandletdie, framework)
    world.path = os.path.join(os.path.dirname(__file__), '../../../sample_apps', path)

@step('When I launch that application wit the subcommand ([\w/.]*)')
@skip_on_py3k.call
def when_i_launch_that_application_wit_the_subcommand_subcommand(step, dev_appserver_path):
    
    port = 8001
    
    if dev_appserver_path:
        world.app = world.AppClass(dev_appserver_path,
                                   world.path,
                                   port=port,
                                   kill_orphans=True)
    else:
        world.app = world.AppClass(world.path, port=port)
    
    world.app.live(kill=True)
    


@step("When I go to the app's url")
@skip_on_py3k.call
def when_i_go_to_the_app_s_url(step):
    world.browser.get(world.app.url)


@step('Then I see "(.*)"')
@skip_on_py3k.call
def then_i_see_text(step, text):
    page_text = world.browser.find_element_by_tag_name('body').text    
    assert text in page_text
    world.app.die()
