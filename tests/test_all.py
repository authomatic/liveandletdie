import os

import liveandletdie


HERE = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(HERE, '..'))
SAMPLE_APPS_DIR = os.path.join(PROJECT_PATH, 'sample_apps')


class Base(object):
    def teardown(cls):
        liveandletdie.port_in_use(8001, kill=True)

    def test_default_url(self, scheme='http', **kwargs):
        app = self.class_(self.app_path, **kwargs)
        assert app.default_url == '{0}://127.0.0.1:8001'.format(scheme)

        app = self.class_(self.app_path, port=1234, **kwargs)
        assert app.default_url == '{0}://127.0.0.1:1234'.format(scheme)

        app = self.class_(self.app_path, host='123.456.789.123', **kwargs)
        assert app.default_url == '{0}://123.456.789.123:8001'.format(scheme)

        app = self.class_(self.app_path, host='123.456.789.123',
                          port=1234, **kwargs)
        assert app.default_url == '{0}://123.456.789.123:1234'.format(scheme)

    def test__normalize_check_url(self, scheme='http', **kwargs):
        # Default url
        app = self.class_(self.app_path, **kwargs)
        normalixed = app._normalize_check_url('http://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com:5555')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        # Custom port
        app = self.class_(self.app_path, port=1234, **kwargs)
        normalixed = app._normalize_check_url('http://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com:5555')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)

        # Custom host
        app = self.class_(self.app_path, host='123.456.789.123', **kwargs)
        normalixed = app._normalize_check_url('http://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com:5555')
        assert normalixed == '{0}://foo.bar.com:8001'.format(scheme)

        # Custom host and port
        app = self.class_(self.app_path, host='123.456.789.123',
                          port=1234, **kwargs)
        normalixed = app._normalize_check_url('http://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)

        normalixed = app._normalize_check_url('https://foo.bar.com:5555')
        assert normalixed == '{0}://foo.bar.com:1234'.format(scheme)


class SSLBase(Base):
    def test_default_url(self):
        super(SSLBase, self).test_default_url()
        super(SSLBase, self).test_default_url('https', ssl=True)

    def test__normalize_check_url(self):
        super(SSLBase, self).test__normalize_check_url()
        super(SSLBase, self).test__normalize_check_url('https', ssl=True)


class TestFlask(SSLBase):
    app_path = os.path.join(SAMPLE_APPS_DIR, 'flask', 'main.py')
    class_ = liveandletdie.Flask

class TestPyramid(SSLBase):
    app_path = os.path.join(SAMPLE_APPS_DIR, 'pyramid', 'main.py')
    class_ = liveandletdie.Pyramid
