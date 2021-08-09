from __future__ import print_function
import argparse
from datetime import datetime
import os
import re
import signal
import ssl
import subprocess
import sys
import tempfile
import time
from werkzeug.serving import make_ssl_devcert
# pylint: disable=wrong-import-order
try:
    from urllib.parse import urlsplit, splitport
except ImportError:
    from urllib2 import splitport
    from urlparse import urlsplit
import requests


_VALID_HOST_PATTERN = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}([:]\d+)?$'


class LiveAndLetDieError(BaseException):
    pass


def _log(logging, message):
    if logging:
        print('LIVEANDLETDIE: {0}'.format(message))


def _validate_host(host):
    if re.match(_VALID_HOST_PATTERN, host):
        return host
    else:
        raise argparse.ArgumentTypeError('{0} is not a valid host!'
                                         .format(host))


def split_host(host):
    """
    Splits host into host and port.

    :param str host:
        Host including port.

    :returns:
        A ``(str(host), int(port))`` tuple.
    """

    host, port = (host.split(':') + [None])[:2]
    return host, int(port)


def check(server):
    """Checks whether a server is running."""
    return server.check()


def live(app):
    """
    Starts a live app in a separate process
    and checks whether it is running.
    """
    return app.live()


def start(*args, **kwargs):
    """Alias for :funct:`live`"""
    live(*args, **kwargs)


def die(app):
    """
    Starts a live app in a separate process
    and checks whether it is running.
    """
    return app.live()


def stop(*args, **kwargs):
    """Alias for :funct:`die`"""
    die(*args, **kwargs)


def port_in_use(port, kill=False, logging=False):
    """
    Checks whether a port is free or not.

    :param int port:
        The port number to check for.

    :param bool kill:
        If ``True`` the process will be killed.

    :returns:
        The process id as :class:`int` if in use, otherwise ``False`` .
    """

    command_template = 'lsof -iTCP:{0} -sTCP:LISTEN'
    process = subprocess.Popen(command_template.format(port).split(),
                               stdout=subprocess.PIPE)
    headers = process.stdout.readline().decode().split()

    if 'PID' not in headers:
        _log(logging, 'Port {0} is free.'.format(port))
        return False

    index_pid = headers.index('PID')
    index_cmd = headers.index('COMMAND')
    row = process.stdout.readline().decode().split()
    if len(row) < index_pid:
        _log(logging, 'Port {0} is free.'.format(port))
        return False

    pid = int(row[index_pid])
    command = row[index_cmd]

    if pid and command.startswith('python'):
        _log(logging, 'Port {0} is already being used by process {1}!'
             .format(port, pid))

        if kill:
            _log(logging,
                 'Killing process with id {0} listening on port {1}!'
                 .format(pid, port))
            os.kill(pid, signal.SIGKILL)

            # Check whether it was really killed.
            try:
                # If still alive
                kill_process(pid, logging)
                # call me again
                _log(logging,
                     'Process {0} is still alive! checking again...'
                     .format(pid))
                return port_in_use(port, kill)
            except OSError:
                # If killed
                return False
        else:
            return pid


def kill_process(pid, logging=False):
    try:
        _log(logging, 'Killing process {0}!'.format(pid))
        os.kill(int(pid), signal.SIGKILL)
        return
    except OSError:
        # If killed
        return False


def _get_total_seconds(td):
    """
    Fixes the missing :meth:`datetime.timedelta.total_seconds()`
    method in Python 2.6
    """
    # pylint: disable=invalid-name

    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) \
        / 10 ** 6


class Base(object):
    """
    Base class for all frameworks.

    :param str path:
        Absolute path to app directory or module (depends on framework).

    :param str host:
        A host at which the live server should listen.

    :param float timeout:
        Timeout in seconds for the check.

    :param str check_url:
        URL where to check whether the server is running.
        Default is ``"http://{host}:{port}"``.

    :param bool logging:
        Whether liveandletdie logs should be printed out.

    :param bool suppress_output:
        Whether the stdout of the launched application should be suppressed.
    """

    _argument_parser = argparse.ArgumentParser()

    def __init__(self, path, host='127.0.0.1', port=8001, timeout=10.0,
                 check_url=None, executable='python', logging=False,
                 suppress_output=True, **kwargs):

        self.path = path
        self.timeout = timeout
        self.host = host
        self.port = port
        self.process = None
        self.executable = executable
        self.logging = logging
        self.suppress_output = suppress_output
        self.check_url = 'http://{0}:{1}'.format(host, port)
        self.scheme = 'http'
        if check_url:
            self.check_url = self._normalize_check_url(check_url)

    def create_command(self):
        pass

    @property
    def default_url(self):
        return '{0}://{1}:{2}'.format(self.scheme, self.host, self.port)

    def _kill(self):
        if self.process:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except OSError:
                self.process.kill()
        self.process.wait()

    def _normalize_check_url(self, check_url):
        """
        Normalizes check_url by:

        * Adding the `http` scheme if missing
        * Adding or replacing port with `self.port`
        """

        # TODO: Write tests for this method
        split_url = urlsplit(check_url)
        host = splitport(split_url.path or split_url.netloc)[0]
        return '{0}://{1}:{2}'.format(self.scheme, host, self.port)

    def check(self, check_url=None):
        """
        Checks whether a server is running.

        :param str check_url:
            URL where to check whether the server is running.
            Default is ``"http://{self.host}:{self.port}"``.
        """

        if check_url is not None:
            self.check_url = self._normalize_check_url(check_url)

        response = None
        sleeped = 0.0
        now = datetime.now()

        while not response:
            try:
                response = requests.get(self.check_url, verify=False)
            except requests.exceptions.ConnectionError:
                if sleeped > self.timeout:
                    self._kill()
                    raise LiveAndLetDieError(
                        '{0} server {1} didn\'t start in specified timeout {2} '
                        'seconds!\ncommand: {3}'.format(
                            self.__class__.__name__,
                            self.check_url,
                            self.timeout,
                            ' '.join(self.create_command())
                        )
                    )
                time.sleep(1)
                sleeped = _get_total_seconds(datetime.now() - now)

        return _get_total_seconds(datetime.now() - now)

    def live(self, kill_port=False, check_url=None):
        """
        Starts a live server in a separate process
        and checks whether it is running.

        :param bool kill_port:
            If ``True``, processes running on the same port as ``self.port``
            will be killed.

        :param str check_url:
            URL where to check whether the server is running.
            Default is ``"http://{self.host}:{self.port}"``.
        """

        pid = port_in_use(self.port, kill_port)

        if pid:
            raise LiveAndLetDieError(
                'Port {0} is already being used by process {1}!'
                .format(self.port, pid)
            )

        host = str(self.host)
        if re.match(_VALID_HOST_PATTERN, host):
            with open(os.devnull, "w") as devnull:
                if self.suppress_output:
                    self.process = subprocess.Popen(self.create_command(),
                                                    stderr=devnull,
                                                    stdout=devnull,
                                                    preexec_fn=os.setsid)
                else:
                    self.process = subprocess.Popen(self.create_command(),
                                                    preexec_fn=os.setsid)

            _log(self.logging, 'Starting process PID: {0}'
                 .format(self.process.pid))
            duration = self.check(check_url)
            _log(self.logging,
                 'Live server started in {0} seconds. PID: {1}'
                 .format(duration, self.process.pid))
            return self.process
        else:
            raise LiveAndLetDieError('{0} is not a valid host!'.format(host))

    def start(self, *args, **kwargs):
        """Alias for :meth:`.live`"""
        self.live(*args, **kwargs)

    def die(self):
        """Stops the server if it is running."""
        if self.process:
            _log(self.logging,
                 'Stopping {0} server with PID: {1} running at {2}.'
                 .format(self.__class__.__name__, self.process.pid,
                         self.check_url))

            self._kill()

    def stop(self, *args, **kwargs):
        """Alias for :meth:`.die`"""
        self.die(*args, **kwargs)

    @classmethod
    def _add_args(cls):
        cls._argument_parser.add_argument('--liveandletdie',
                                          help='Run as test live server.',
                                          type=_validate_host,
                                          nargs='?',
                                          const='170.0.0.1:5000')

    @classmethod
    def parse_args(cls, logging=False):
        """
        Parses command line arguments.

        Looks for --liveandletdie [host]

        :returns:
            A ``(str(host), int(port))`` or ``(None, None)`` tuple.
        """

        cls._add_args()
        args = cls._argument_parser.parse_args()

        if args.liveandletdie:
            _log(logging, 'Running as test live server at {0}'
                 .format(args.liveandletdie))
            return split_host(args.liveandletdie)
        else:
            return None, None


class WrapperBase(Base):
    """Base class for frameworks that require their app to be wrapped."""

    def create_command(self):
        return [
            self.executable,
            self.path,
            '--liveandletdie',
            '{0}:{1}'.format(self.host, self.port),
        ]


class Flask(WrapperBase):
    def __init__(self, *args, **kwargs):
        """
        :param bool ssl:
            If true, the app will be run with ``ssl_context="adhoc"`` and the
            schema of the ``self.check_url`` will be ``"https"``.
        """
        self.ssl = kwargs.pop('ssl', None)
        super(Flask, self).__init__(*args, **kwargs)
        if self.ssl:
            self.scheme = 'https'

    @classmethod
    def _add_args(cls):
        super(Flask, cls)._add_args()
        cls._argument_parser.add_argument('--ssl',
                                          help='Run with "adhoc" ssl context.',
                                          type=bool,
                                          nargs='?',
                                          default=False)

    def create_command(self):
        command = super(Flask, self).create_command()
        if self.ssl is True:
            command += ['--ssl=1']
        return command

    def check(self, check_url=None):
        url = self.check_url if check_url is None else \
            self._normalize_check_url(check_url)

        if self.ssl:
            url = url.replace('http://', 'https://')

        super(Flask, self).check(url)

    @classmethod
    def wrap(cls, app):
        """
        Adds test live server capability to a Flask app module.

        :param app:
            A :class:`flask.Flask` app instance.
        """

        host, port = cls.parse_args()
        ssl_context = None

        if host:
            if cls._argument_parser.parse_args().ssl:
                try:
                    import OpenSSL  # pylint: disable=unused-variable
                except ImportError:
                    # OSX fix
                    sys.path.append(
                        '/System/Library/Frameworks/Python.framework/Versions/'
                        '{0}.{1}/Extras/lib/python/'
                        .format(sys.version_info.major, sys.version_info.minor)
                    )

                try:
                    import OpenSSL  # pylint: disable=unused-variable
                except ImportError:
                    # Linux fix
                    sys.path.append(
                        '/usr/lib/python{0}.{1}/dist-packages/'
                        .format(sys.version_info.major, sys.version_info.minor)
                    )

                try:
                    import OpenSSL  # pylint: disable=unused-variable
                except ImportError:
                    raise LiveAndLetDieError(
                        'Flask app could not be launched because the pyopenssl '
                        'library is not installed on your system!'
                    )
                ssl_context = 'adhoc'

            app.run(host=host, port=port, ssl_context=ssl_context)
            sys.exit()


class GAE(Base):
    def __init__(self, dev_appserver_path, *args, **kwargs):
        """
        :param str dev_appserver:
            Path to dev_appserver.py

        """
        super(GAE, self).__init__(*args, **kwargs)
        self.dev_appserver_path = dev_appserver_path
        self.admin_port = kwargs.get('admin_port', 5555)

    def create_command(self):
        command = [
            self.dev_appserver_path,
            '--host={0}'.format(self.host),
            '--port={0}'.format(self.port),
            '--admin_port={0}'.format(self.admin_port),
            '--skip_sdk_update_check=yes',
            self.path
        ]

        if self.dev_appserver_path.endswith(('.py', '.pyc')):
            command = [self.executable] + command
        return command


class WsgirefSimpleServer(WrapperBase):
    def __init__(self, *args, **kwargs):
        """
        :param bool ssl:
            If true, the app will be run with ssl enabled and the
            scheme of the ``self.check_url`` will be ``"https"``.
        """
        self.ssl = kwargs.pop('ssl', None)
        super(WsgirefSimpleServer, self).__init__(*args, **kwargs)
        if self.ssl:
            self.scheme = 'https'

    def create_command(self):
        command = super(WsgirefSimpleServer, self).create_command()
        if self.ssl is True:
            command += ['--ssl=1']
        return command

    def check(self, check_url=None):
        url = self.check_url if check_url is None else \
            self._normalize_check_url(check_url)

        if self.ssl:
            url = url.replace('http://', 'https://')

        super(WsgirefSimpleServer, self).check(url)

    @classmethod
    def _add_args(cls):
        super(WsgirefSimpleServer, cls)._add_args()
        cls._argument_parser.add_argument('--ssl',
                                          help='Run with ssl enabled.',
                                          type=bool,
                                          nargs='?',
                                          default=False)

    @classmethod
    def wrap(cls, app):
        host, port = cls.parse_args()
        if host:
            from wsgiref.simple_server import make_server

            server = make_server(host, port, app)
            if cls._argument_parser.parse_args().ssl:
                # Set HTTPS='1' makes wsgiref set wsgi.url_scheme='https'
                # This in turn makes pyramid set request.scheme='https'
                server.base_environ['HTTPS'] = '1'

                with tempfile.TemporaryDirectory() as td:
                    # Generate temporary self-signed cert/key pair
                    # using the library used by Flask for 'adhoc' ssl_context
                    certpath = '{}/liveandletdie'.format(td)
                    make_ssl_devcert(certpath)

                    server.socket = ssl.wrap_socket(
                        server.socket,
                        server_side=True,
                        certfile='{}.crt'.format(certpath),
                        keyfile='{}.key'.format(certpath),
                    )

            server.serve_forever()
            server.server_close()
            sys.exit()


class Django(Base):
    def create_command(self):
        return [
            self.executable,
            os.path.join(self.path, 'manage.py'),
            'runserver',
            '{0}:{1}'.format(self.host, self.port),
        ]


class FastAPIServer(Base):
    def __init__(self, *args, **kwargs):
        kwargs['executable'] = 'uvicorn'
        super().__init__(*args, **kwargs)

    def create_command(self):
        return [
            self.executable,
            '{}:app'.format(self.path),
            '--host {}'.format(self.host),
            '--port {}'.format(self.port),
            '--reload',
        ]
