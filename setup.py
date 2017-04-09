# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

from rapidfire import (
    __version__,
    __license__,
    __author__,
    __author_email__,
)

__name__ = 'rapidfire'
__url__ = 'https://github.com/wanshot/RapidFire'

__short_description__ = __name__ + ' calls and displays the defined Python function from command line'
__long_description__ = open('./README.rst', 'r').read()

__classifiers__ = [
    'Programming Language :: Python',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development',
    'Programming Language :: Python :: 3',
    'Topic :: Terminals',
]

__keywords__ = [
    'cli',
    'command line interface',
    'shell',
]

setup(
    name=__name__,
    version=__version__,
    description=__short_description__,
    long_description=__long_description__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    classifiers=__classifiers__,
    keywords=' ,'.join(__keywords__),
    license=__license__,
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['rap = rapidfire.run:main']
    },
    install_requires=['wcwidth'],
)
