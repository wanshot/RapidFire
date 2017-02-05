# -*- coding:utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='rapid_fire',
    version='0.0.0',
    author='wanshot',
    author_email='',
    description='',
    license='MIT',
    keywords='',
    long_description=read('README.md'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=['rapid_fire'],
    entry_points={
        'console_scripts': ['rf = rapid_fire.run:main']
    },
    install_requires=['argparse', 'six'],
)