# -*- coding:utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='rapidfire',
    version='0.0.0',
    author='wanshot',
    author_email='',
    description='',
    license='MIT',
    keywords='',
    long_description=read('README.rst'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=['rapidfire'],
    entry_points={
        'console_scripts': ['rap = rapidfire.run:main']
    },
    install_requires=['argparse', 'six', 'wcwidth'],
)
