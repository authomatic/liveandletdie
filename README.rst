================
Live and Let Die
================
.. image:: https://travis-ci.org/peterhudec/liveandletdie.svg?branch=master
    :target: https://travis-ci.org/peterhudec/liveandletdie

**Live and Let Die** simplifies launching and terminating of web development
servers from **BDD** or **functional** tests. I have created it for functional
testing of the `Authomatic <peterhudec.github.io/authomatic/>`_ package.

The package Currently supports **Google App engine**, **Django**,
**Flask** and **wsgiref.simple_server**. Support for other frameworks will
hopefully be added in future.

Usage
-----

You first need to make instance of one of the framework classes.

Django
^^^^^^

.. code-block:: python

    import liveandletdie

    # Django
    app = liveandletdie.Django('path/to/django/project/',
                               host='0.0.0.0',
                               port=5555)

Google App Engine
^^^^^^^^^^^^^^^^^

.. code-block:: python

    import liveandletdie

    app = liveandletdie.GAE('path/to/dev_appserver.py',
                            'path/to/gae/app/dir', # containing app.yaml file
                            host='0.0.0.0',
                            port=5555)

Flask
^^^^^

By **Flask** you must wrap the **WSGI application** in
``liveandletdie.Flask.wrap(app)``.

If you set the ``ssl`` keyword argument to ``True``, the app will be run with
``ssl_context="adhoc"`` and the schema of the ``self.check_url``
will be ``"https"``.

.. note::

    If you are struggling with installation of
    `pyOpenSSL <https://pypi.python.org/pypi/pyOpenSSL>`__ on OSX due to
    ``'ffi.h' file not found`` error during installation of the
    `cryptography <https://pypi.python.org/pypi/cryptography/0.7.2>`__
    dependency, try the solution from this
    `Stackoverflow question <http://stackoverflow.com/questions/22875270/error-installing-bcrypt-with-pip-on-os-x-cant-find-ffi-h-libffi-is-installed>`__:

    .. code-block:: bash

        $ brew install pkg-config libffi
        $ export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/
        $ pip install pyopenssl

.. code-block:: python

    # flask/app/main.py
    from flask import Flask

    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

    app = Flask(__name__)
    app.config.from_object(__name__)

    @app.route('/')
    def home():
        return 'Hello World!'

    if __name__ == '__main__':

        # This does nothing unless you run this module with --liveandletdie flag.
        import liveandletdie
        liveandletdie.Flask.wrap(app)

        app.run()


.. code-block:: python

    import liveandletdie

    app = liveandletdie.Flask('path/to/flask/app/main.py',
                              host='0.0.0.0',
                              port=5555)

Pyramid (wsgiref.simple_server)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By ``wsgiref.simple_server`` you must wrap the **WSGI application** in
``liveandletdie.WsgirefSimpleServer.wrap(app)``.

If you set the ``ssl`` keyword argument to ``True``, the app will be run with
a self-signed certificate, and the schema of the ``self.check_url``
will be ``"https"``.

.. code-block:: python

    # pyramid/app/main.py
    from wsgiref.simple_server import make_server

    from pyramid.config import Configurator
    from pyramid.response import Response


    def home(request):
        return Response('Hello World!')


    if __name__ == '__main__':

        config = Configurator()
        config.add_route('home', '/')
        config.add_view(home, route_name='home')
        app = config.make_wsgi_app()

        # This does nothing unless you run this module with --liveandletdie flag.
        import liveandletdie
        liveandletdie.WsgirefSimpleServer.wrap(app)

        server = make_server('127.0.0.1', 8080, app)
        server.serve_forever()


.. code-block:: python

    import liveandletdie

    app = liveandletdie.Flask('path/to/pyramid/app/main.py',
                              host='0.0.0.0',
                              port=5555)

Using the App instance
^^^^^^^^^^^^^^^^^^^^^^

The interface is the same for all of the supported frameworks.

.. code-block:: python

    # Start the app.
    # If kill_port is True,
    # it will kill any process listening on port 5555
    process = app.live(kill_port=True)

    # You can check whether it is running
    is_running = app.check()

    # Stop it
    app.die()

Simple UnitTest example:
https://github.com/peterhudec/liveandletdie/blob/master/test_examples/unittest_example/tests.py

Simple PyTest example:
https://github.com/peterhudec/liveandletdie/blob/master/test_examples/pytest_example/tests.py

Simple Lettuce example:
https://github.com/peterhudec/liveandletdie/blob/master/test_examples/lettuce_example/tests.py

Debugging
---------

If an app refuses to start on the ``app.live()`` call, it throws a
``LiveAndLetDieError`` with a message::

    Flask server https://127.0.0.1:5555 didn't start in specified timeout 10.0 seconds!
    command: python sample_apps/flask/main.py --liveandletdie 127.0.0.1:5555

To find out more about why the app didn't start run the command provided in the
error message manually:

.. code-block:: bash

    $ python sample_apps/flask/main.py --liveandletdie 127.0.0.1:5555

Developers
----------

Clone:

::
    
    $ git clone https://github.com/peterhudec/liveandletdie.git

Bootstrap the development environment.
This will create the ``./venv`` virtual environment in the project root.

::
    
    $ sh bootstrap.sh

Run tests:

::
    
    $ sh run-all.sh

Or bootstrap and run tests in one step:

::

    $ sh bootstrap-and-test.sh

Enjoy!
