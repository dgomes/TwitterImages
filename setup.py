# -*- coding: utf-8 -*-
"""setup.py"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
]

def read_content(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_description = (
    read_content("README.rst")) 

requires = ['setuptools']

with open('requirements.txt', 'w') as _file:
    _file.write('\n'.join(requires))

setup(name='twitterimages',
      version='0.1.0',
      description='Twitter Bot to post random images from a directory',
      long_description=long_description,
      author='Diogo Gomes',
      author_email='diogogomes@gmail.com',
      url='https://github.com/dgomes/twitterimages',
      classifiers=classifiers,
      packages=['twitterimages'],
      data_files=[],
      install_requires=requires,
      include_package_data=True,)
