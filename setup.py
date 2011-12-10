#!/usr/bin/env python

from distutils.core import setup

setup(
    name='calculon',
    version='1.0',
    author='Nikita Pchelin',
    author_email='nikita.pchelin@gmail.com',
    url='https://github.com/jango/calculon',
    description=r"Customizable implementation of the producer-consumer pattern using Python's multiprocessing module.",
    classifiers = ['Classifier: Development Status :: 5 - Production/Stable',
                   'Classifier: License :: OSI Approved :: MIT License'],
    py_modules = ['calculon.calculon', 'calculon.calculon-example'],
)


