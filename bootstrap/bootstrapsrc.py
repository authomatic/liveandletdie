import os
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
import zipfile
import platform
import sys


CHROMEDRIVER_VERSION = '2.12'
CHROMEDRIVER_PATH_BASE = 'http://chromedriver.storage.googleapis.com/{0}/'\
    .format(CHROMEDRIVER_VERSION)

ARCHITECTURE = platform.architecture()[0][:-3]
PLATFORM = platform.platform()


def after_install(options, home_dir):
    bootstrap_root = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(bootstrap_root, '..'))

    def _download_and_extract(url, extract_path):
        print('Downloading {0}'.format(url))
        tmp_zip_path = urlretrieve(url)[0]
        zf = zipfile.ZipFile(tmp_zip_path)

        extract_path = os.path.join(home_dir, extract_path)
        extract_path = os.path.abspath(extract_path)
        print('Extracting {0} to {1}'.format(tmp_zip_path, extract_path))
        zf.extractall(os.path.join(home_dir, extract_path))

    def _add_pth(name, content):
        python_version = '{0}.{1}'.format(*sys.version_info)
        pth_path = 'lib/python{0}/site-packages/{1}.pth'\
            .format(python_version, name)
        with open(os.path.join(home_dir, pth_path), 'w') as pth:
            print('Creating PTH file: {0}'.format(os.path.abspath(pth_path)))
            pth.writelines(content)

    if PLATFORM.lower().startswith('darwin'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + 'chromedriver_mac32.zip'
    elif PLATFORM.lower().startswith('linux'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + \
            'chromedriver_linux{0}.zip'.format(ARCHITECTURE)
    elif PLATFORM.lower().startswith('win'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + 'chromedriver_win32.zip'
    else:
        chromedriver_path = None

    if chromedriver_path:
        _download_and_extract(chromedriver_path, 'bin')
        chromedriver_executable = os.path.join(home_dir, 'bin/chromedriver')
        print('Setting permissions of {0} to 755'
              .format(chromedriver_executable))
        os.chmod(chromedriver_executable, 755)

    _add_pth('liveandletdie', project_root)
