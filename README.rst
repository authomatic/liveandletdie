================
Test Live Server
================

**Test Live Server** is a very simple utility for running
a Flask development server for **BDD/functional** testing purposes.

I'm planning to add support for other frameworks in future.

Usage
-----

Add the **Test Live Server** capability to your Flask app by calling the
:func:`.live_server` function just before the ``app.run()``.

.. literalinclude:: sample_apps/flask_sample/main.py

In your test setup call the :func:`.start` function which returns the process of the running app
which you can terminate in the teardown.

.. literalinclude:: test_examples/unittest_example/tests.py