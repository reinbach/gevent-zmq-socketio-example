#!/usr/bin/env python
from setuptools import setup

requires = [
    'Flask==0.8',
    'gevent==0.13.7',
    'gevent-socketio==0.3.5-beta',
    'pyzmq==2.2.0',
]

setup(
    name='Gevent SocketIO Example',
    version='1.0',
    description='Mini app using gevent and socketio',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/gevent-socketio-example',
    install_requires=requires,
)