#!/usr/bin/env python3

'''
Setup script for python build system
'''
import os
from setuptools import setup, find_packages

from lnxproc import about

HERE = os.path.abspath(os.path.dirname(__file__))
NAME = open('name', 'rt').read().strip()

REQFILE = os.extsep.join(['requirements', 'txt'])
with open(REQFILE, 'rt', ) as FF:
    REQUIREMENTS = [
        i.strip() for i in FF
        if not (i.startswith('#') or i.startswith('-'))
    ]

with open('README.md') as FF:
    DESC = FF.read()

setup(
    name=NAME,
    version=about.__version__,
    packages=find_packages(exclude=("unittests", )),
    license=about.__license__,
    description=about.__description__,
    long_description=DESC,
    url='https://github.com/eccles/' + NAME + '/',
    download_url='https://github.com/eccles/' + NAME + '/dist/',
    author=about.__author__,
    author_email=about.__author_email__,
    platforms=['linux', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Systems Monitoring'
    ],
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'lnxproc = lnxproc:entry.main',
        ],
    },
)
