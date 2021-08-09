from setuptools import setup,find_packages
import os


NAME = 'liveandletdie'
HERE = os.path.dirname(__file__)


setup(
    name=NAME,
    version='0.0.8',
    packages=find_packages(),
    install_requires=['requests', 'werkzeug'],
    package_data={'': ['*.txt', '*.rst']},
    author='Peter Hudec',
    author_email='peterhudec@peterhudec.com',
    maintainer='Authomatic Project Community',
    maintainer_email='authomaticproject@protonmail.com',
    description='Simplifies launching and terminating of web development '
        'servers from BDD and functional tests.',
    long_description=open(os.path.join(HERE, 'README.rst')).read(),
    keywords='Flask, Pyramid, Django, Google App Engine, GAE, BDD, TDD, '
        'functional testing, live server',
    url='http://github.com/peterhudec/{0}'.format(NAME),
    license = 'MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: '
            'CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
