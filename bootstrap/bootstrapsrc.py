import os
import urllib
import zipfile
import platform


CHROMEDRIVER_VERSION = '2.8'
GAE_SDK_VERSION = '1.8.3'
CHROMEDRIVER_PATH_BASE = 'http://chromedriver.storage.googleapis.com/{}/'\
    .format(CHROMEDRIVER_VERSION)

ARCHITECTURE = platform.architecture()[0][:-3]
PLATFORM = platform.platform()


def after_install(options, home_dir):
    bootstrap_root = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(bootstrap_root, '..'))

    def _download_and_extract(url, extract_path):
        print('Downloading {}'.format(url))
        tmp_zip_path = urllib.urlretrieve(url)[0]
        zf = zipfile.ZipFile(tmp_zip_path)

        extract_path = os.path.join(home_dir, extract_path)
        extract_path = os.path.abspath(extract_path)
        print('Extracting {} to {}'.format(tmp_zip_path, extract_path))
        zf.extractall(os.path.join(home_dir, extract_path))

    def _add_pth(name, content):
        pth_path = 'lib/python2.7/site-packages/{}.pth'.format(name)
        with open(os.path.join(home_dir, pth_path), 'w') as pth:
            print('Creating PTH file: {}'.format(os.path.abspath(pth_path)))
            pth.writelines(content)

    if PLATFORM.lower().startswith('darwin'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + 'chromedriver_mac32.zip'
    elif PLATFORM.lower().startswith('linux'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + \
            'chromedriver_linux{}.zip'.format(ARCHITECTURE)
    elif PLATFORM.lower().startswith('win'):
        chromedriver_path = CHROMEDRIVER_PATH_BASE + 'chromedriver_win32.zip'
    else:
        chromedriver_path = None

    if chromedriver_path:
        _download_and_extract(chromedriver_path, 'bin')
        chromedriver_executable = os.path.join(home_dir, 'bin/chromedriver')
        print('Setting permissions of {} to 755'
              .format(chromedriver_executable))
        os.chmod(chromedriver_executable, 755)

    _download_and_extract('http://googleappengine.googlecode.com/files/' +
                          'google_appengine_{}.zip'.formal(GAE_SDK_VERSION),
                          'bin')

    _add_pth('liveandletdie', project_root)
    _add_pth('gae', '\n'.join([
            os.path.abspath(os.path.join(home_dir, 'bin/google_appengine/')),
            'import dev_appserver',
            'dev_appserver.fix_sys_path()',
        ]))