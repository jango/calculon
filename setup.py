#!/usr/bin/env python
import os
#from distutils.core import setup
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='calculon',
    version='1.1',
    author='Nikita Pchelin',
    author_email='nikita.pchelin@gmail.com',
    url='https://github.com/jango/calculon',
    description=r"Customizable implementation of the producer-consumer pattern using Python's multiprocessing module.",
    long_description=read('README.md'),
    classifiers = ['Classifier: Development Status :: 5 - Production/Stable',
                   'Classifier: License :: OSI Approved :: MIT License'],
    packages=find_packages(exclude=['tests']),
    package_data = {
        'calculon': ['LICENSE', 'README.md5', 'RELEASE']
    },
    include_package_date=True,
    test_suite="tests",
)
