from setuptools import setup,find_packages

setup(
    name='TestLiveServer',
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst']},
    author='Peter Hudec',
    author_email='peterhudec@peterhudec.com',
    description='Simple utility for running a Flask development server for BDD/functional testing purposes.',
    long_description=open('README.rst').read(),
    keywords='Flask, BDD, TDD, functional testing, live server',
    url='http://github.com/peterhudec/testliveserver',
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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)