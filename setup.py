from setuptools import setup,find_packages

NAME = 'liveandletdie'

setup(
    name=NAME,
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst']},
    author='Peter Hudec',
    author_email='peterhudec@peterhudec.com',
    description='Simplifies launching and terminating of web development '
        'servers from BDD and functional tests.',
    long_description=open('README.rst').read(),
    keywords='Flask, Pyramid, Django, Google App Engine, GAE, BDD, TDD, '
        'functional testing, live server',
    url='http://github.com/peterhudec/{}'.format(NAME),
    license = 'MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: '
            'CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)