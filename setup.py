#!/usr/bin/env python

from setuptools import setup

setup(
    name='simple-deluge',
    version='0.0.1',
    description='Friendly Deluge API built on the RPC interface',
    author='Aaron Tsui',
    author_email='hinfaits@users.noreply.github.com',
    url='https://github.com/hinfaits/simple-deluge',
    packages=['simple_deluge',],
    install_requires=['deluge-client==1.0.5',],
)
