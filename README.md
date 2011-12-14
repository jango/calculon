# Calculon
This project is a customizable implementation of the producer-consumer pattern
using Python's multiprocessing/threading module:

* define a custom producer and a custom consumer function;
* choose between multiprocessing or multithreading option for your calculations;
* instruct the instance to return any information you want to collect back from
the producers and consumer;

I wrote this because I needed a simple setup that would allow me to process
simple parallel computing tasks that will not benefit from a heavier approach.

# Install
To install the stable version:
    easy_install calculon
    
Otherwise, you can checkout the current code from ther github repository:
https://github.com/jango/calculon

# Example
Look into **calculon-example.py** for a very simple usage example, look at the
docstings to get more info.

# License
This project was released under MIT license, see **LICENSE** file for more
information.

# Release Notes
See RELEASE file for the release history.