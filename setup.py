#!/usr/bin/env python
#-*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='configbuilder',
    version='0.1',
    url='https://github.com/joongh/configbuilder',
    license='MIT',
    author='Joong-Hee Lee',
    author_email='leejoonghee@gmail.com',
    description='General purpose configuration parser builder',
    package_dir={'configbuilder':''},
    packages=['configbuilder'],
    install_requires=[
        'PyYAML==3.11',
    ],
)
