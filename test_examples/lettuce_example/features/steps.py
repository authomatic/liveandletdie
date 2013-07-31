# -*- coding: utf-8 -*-
from lettuce import *

@step(u'Given a website running at "([^"]*)"')
def given_a_website_running_at(step, location):
    world.website = str(location)

@step(u'When I go to that location')
def when_i_go_to_that_address(step):
    world.browser.get(world.website)
    world.site_content = world.browser.find_element_by_tag_name('body').text

@step(u'Then I see "([^"]*)"')
def then_i_see(step, content):
    assert content in world.site_content
