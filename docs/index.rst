.. Calculon documentation master file, created by
   sphinx-quickstart on Wed Apr  3 22:13:28 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Calculon
========

About
-----
Calculon is inspired by a classic `producer-consumer problem <http://en.wikipedia.org/wiki/Producer-consumer_problem>`_ and a `map-reduce programming model <http://en.wikipedia.org/wiki/Map_reduce>`_. Calculon allows you to configure multiple producer and consumer instances, execute the computation, and get the results back.

Calculon works great for small and medium-sized parallel computing problems, especially if you don't want to employ a heavy framework. The original application of this package was to support web mining. In that case, producers were configured to parse web pages and consumers were configured to store the results in the database.

Calculon has been tested on Windows, Linux, and Cygwin, but it might be helpful to run::

  $ python setup.py test

to verify that threading / multoprocessing works correctly on your platform.

Installation
------------
The easiest way is to install the package through *easy_install*::

  $ easy_install calculon

or *pip*::

  $ pip install calculon

You can also get the stable version of the package on PyPi:
    https://pypi.python.org/pypi/calculon

Alternatively, if you want to see the development version, check it out from GitHub:
    https://github.com/jango/calculon


Example
-------

The full working file of this example can be found in::

    calculon/example/example.py


Producer
~~~~~~~~

Let's start by writing a producer function. It should accept a single argument, a dictionary of parameters passed to it. The code below produces five strings of text by combining two names, one from the list, and one from the arguments list, five times. The producer code is called only once by calculon. The function will also return `Finished!` once it is done running.

.. code-block:: python

    NAMES = ['John', 'Sally', 'Branko', 'Elena', 'Michael']
    VERBS = ['walks', 'plays', 'sings', 'drinks']


    def producer(args):
        for name in NAMES:
            args["_queue"].put("{0} and {1}".format(name, args["extra_name"]))

        return "Finished!"

There are a few "special" arguments in the `args` dictionary available to the producer. More information about on :ref:`producer` page. An extra argument, `extra_name` is one of the arguments that we pass to the producer ourselves when instantiating a Calculon object, which you will see a bit later.


Consumer
~~~~~~~~

Now let's write a consumer. The consumer will take one of the strings from the queue and append two verbs, one selected randomly and one passed to it through `args` parameter. Then, the final result will be printed to the screen. In addition, every time the consumer function runs, it will return how many times it's run so far.

Note that the consumer is called as many times as many values are available for it to process `plus` one time after the queue is empty. This last time is there to allow any sort of cleanup that the consumer might need to do.

.. code-block:: python

    def consumer(args):
        value = args["_value"]
        is_last_call = args["_last_call"]
        result = args["_result"]

        time.sleep(random.randint(0, 3))

        # You should never assume that the consumer instance
        # will get at least one value from the queue. If you
        # have too many consumers running, some of them can
        # get shutdown before they get a chance to process
        # a single value.
        if result is None and is_last_call:
            return 0

        # In two other cases, we just need to check if it's
        # our last cleanup call or not.
        if not is_last_call:
            print "{0} {1} and {2}.".format(value, random.choice(VERBS), args["extra_action"])

            if result is None:
                return 1
            else:
                return result + 1
        else:
            return result

There are a few predefined arguments in the `args` dictionary. More information on those can be found on :ref:`consumer` page.


Running Calculon
~~~~~~~~~~~~~~~~

Finally, let's put these two pieces together by instantiating a Calculon object and starting it:

.. code-block:: python

    pp = pprint.PrettyPrinter(indent=4)

    calculon = Calculon(producer,
                        [{"extra_name": "Tania"}],
                        True,
                        consumer,
                        [{"extra_action": "dances"}, {"extra_action": "sleeps"}],
                        True)

    result = calculon.start()

    pp.pprint(result)

The first and fourth parameters are the producer and the consumer functions that we just wrote. The second and fifth are lists of arguments for the producers and consumers. As you can see, we asked for one producer and two consumers. The third and sixth parameters specify what type of multiprocessing to use threads (if the value is `True`) or processes. More information about these parameters can be found on :ref:`calculon` page.

Result
~~~~~~

When you run the sample code, your output will look something like that:

.. code-block:: bash

    jango@sunblaze:~/workspace/calculon/calculon/example$ python example.py
    John and Tania sings and dances.
    Branko and Tania sings and dances.
    Sally and Tania walks and sleeps.
    Michael and Tania walks and sleeps.
    Elena and Tania walks and dances.
    {   'consumers': [   {   'name': '91cecb8c9d8411e2b78100241dd35a03',
                             'result': 3},
                         {   'name': '91cf25dc9d8411e2b78100241dd35a03',
                             'result': 2}],
        'producers': [   {   'name': '91ce694e9d8411e2b78100241dd35a03',
                             'result': 'Finished!'}]}

In this case, the first consumer processed three records and the other one processed three. All five generated sentences are also printed on the screen.


Handling Exceptions
~~~~~~~~~~~~~~~~~~~

If a call to your producer / consumer functions results in an exception, this is what you will get instead:

.. code-block:: bash

    jango@sunblaze:~/workspace/calculon/calculon/example$ python example.py
    {   'consumers': [   {   'exception': ZeroDivisionError('integer division or modulo by zero',),
                             'name': 'dcf9cdbe9d8411e283ef00241dd35a03'},
                         {   'exception': ZeroDivisionError('integer division or modulo by zero',),
                             'name': 'dcfa2d2c9d8411e283ef00241dd35a03'}],
        'producers': [   {   'name': 'dcf967f29d8411e283ef00241dd35a03',
                             'result': 'Finished!'}]}


Note that you can use the exception object returned to obtain more information about the problem.

More Info
---------
The example section contains most of the functionality available through this package. If you are looking for something more, dive into the :ref:`autodoc` or ask the author.

Author
------
The project is written and maintained by Nikita Pchelin. Contact information is provided on the `GitHub <https://github.com/jango>`_ page.

License
-------
The project is distributed under the `MIT license <http://opensource.org/licenses/MIT>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`