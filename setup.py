#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from setuptools import setup, find_packages
import os
import proteus_startup

PREFIX = 'nantic'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require

name = 'proteus_startup'
version = proteus_startup.__version__
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

dependency_links = []
if minor_version % 2:
    # Add development index for testing with trytond
    dependency_links.append('https://trydevpi.tryton.org/')

setup(name='%s_%s' % (PREFIX, name),
    version=version,
    description='A library with functions to get and/or create Tryton model instances',
    long_description=read('README'),
    author='NaN·tic',
    url='http://www.nan-tic.com/',
    download_url="https://bitbucket.org/nantic/%s" % name,
    keywords='tryton library tests',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: '
        'GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        ],
    platforms='any',
    license='LGPL-3',
    install_requires=[
        "python-dateutil",
        "proteus >= %s.%s, < %s.%s" %
            (major_version, minor_version, major_version, minor_version + 1)
        ],
    extras_require={
        'trytond': [get_require_version('trytond')],
        'simplejson': ['simplejson'],
        'cdecimal': ['cdecimal'],
        },
    dependency_links=dependency_links,
    zip_safe=True,
    # test_suite='proteus_startup.tests',
    # tests_require=[get_require_version('trytond')],
    )
