Version 0.0.6
-------------

* The ``check()`` method now uses the `requests <python-requests.org>`__ package.

Version 0.0.5
-------------

* Added Python 3 support thanks to
  `Emmanuel Leblond <https://github.com/touilleMan>`_.

Version 0.0.4
-------------

* Fixed a bug when app hung when there was a lot of stdout.

Version 0.0.3
-------------

* The :class:`livenandletdie.GAE` is now more stable.
* Added ssl support for :class:`livenandletdie.Flask`.
* Better error handling.
* Renamed the ``enable_logging`` parameter of constructors to ``logging``.
* Renamed the ``kill`` parameter of the ``die()`` method to ``kill_port``.

Version 0.0.2
-------------

Made compatible with **Python 2.6**.

Version 0.0.1
-------------

Fixed the issue with unsupported ``ps -C`` option in ``GAE._kill_orphans()``.

Version 0.0.0
-------------

Renamed from **Test Live Server** to **Live and Let Die**