#!/usr/bin/env python
#-*- coding: utf-8 -*-
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name='configbuilder',
    version='0.2.2',
    url='https://github.com/joongh/configbuilder',
    license='MIT',
    author='Joong-Hee Lee',
    author_email='leejoonghee@gmail.com',
    description='General purpose configuration parser builder',
    long_description=read('README.md'),
    package_dir={'configbuilder':''},
    packages=['configbuilder'],
    install_requires=[
        'PyYAML==5.1',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
