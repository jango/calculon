#!/usr/bin/env python
import os
from setuptools import setup


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='calculon',
    version='1.1.1',
    author='Nikita Pchelin',
    author_email='nikita@pchelin.ca',
    url='https://github.com/jango/calculon',
    description=r"Implementation of the producer-consumer pattern"
                "with customizable producer and consumer methods and"
                "an ability to choose thread/process model for execution.",
    long_description=read('README.md'),
    classifiers=['Classifier: Development Status :: 5 - Production/Stable',
                 'Classifier: License :: OSI Approved :: MIT License',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: POSIX',
                 'Operating System :: Microsoft :: Windows',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: System :: Distributed Computing'],
    test_suite='calculon.test',
    packages=['calculon', 'calculon.test'],
)
