# -*- coding: utf-8 -*-
from functools import wraps
import os
import sys

from lettuce import step, world
import six
import requests

import liveandletdie


class Skip:

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
            if not self.skip_test:
                return func(step, framework, path)
        return wrapper


skip = Skip()


@step('Given a web application based on (\w+) located at ([\w/.]+)')
@skip.init
def given_a_web_application(step, framework, path):
    world.AppClass = getattr(liveandletdie, framework)

    if framework == 'GAE' and not (six.PY2 and sys.version_info[1] is 7):
        print('GAE not supported on {0}'.format(sys.version))
        skip.skip_test = True

    world.path = os.path.join(os.path.dirname(__file__),
                              '../../../sample_apps', path)


@step('When I launch that application wit the subcommand '
      '([\w/.]*) with (yes|no)')
@skip.call
def when_i_launch_that_application(step, dev_appserver_path, ssl):
    port = 8001
    if dev_appserver_path:
        world.app = world.AppClass(
            '{0}/{1}'.format(os.environ['VIRTUAL_ENV'], dev_appserver_path),
            world.path,
            port=port
        )
    else:
        world.app = world.AppClass(world.path, port=port, ssl=(ssl == 'yes'))

    world.app.live(kill_port=True)


@step("When I go to the app's url")
@skip.call
def when_i_go_to_the_app_s_url(step):
    world.page_text = requests.get(world.app.check_url, verify=False).\
        content.decode('utf-8')


@step('Then I see "(.*)"')
@skip.call
def then_i_see_text(step, text):
    assert text in world.page_text
    world.app.die()
