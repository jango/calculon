#!/usr/bin/env python
import os
#from distutils.core import setup
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='calculon',
    version='1.0',
    author='Nikita Pchelin',
    author_email='nikita.pchelin@gmail.com',
    url='https://github.com/jango/calculon',
    description=r"Customizable implementation of the producer-consumer pattern using Python's multiprocessing module.",
    long_description=read('README'),
    classifiers = ['Classifier: Development Status :: 5 - Production/Stable',
                   'Classifier: License :: OSI Approved :: MIT License'],
    py_modules = ['calculon.calculon', 'calculon.calculon-example'],
    test_suite="tests",
)


