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

Calculon has been tested on Windows, Linux, and Cygwin, but it might be helpful to run:

  $ python setup.py test

to verify that threading / multoprocessing works correctly on your platform.

Install
-------
You can install the package through *easy_install*::

  $ easy_install calculon

or *pip*::

  $ pip install calculon


Example
-------

The full working file of the example can be found in::

    calculon/example/example.py


Writing Producer Function
~~~~~~~~~~~~~~~~~~~~~~~~~

Start by writing a producer function. It should accept a single argument, a dictionary of parameters passed to the function. The code below produces five strings of text by combining two names, one from the list, and one from the arguments list. The producer code is called only once by calculon. The function will also return `Finished!` once it is done running.

.. code:: python

    NAMES = ['John', 'Sally', 'Branko', 'Elena', 'Michael']
    VERBS = ['walks', 'plays', 'sings', 'drinks']


    def producer(args):
        for name in NAMES:
            args["_queue"].put("{0} and {1}".format(name, args["extra_name"]))

        return "Finished!"

There are a few predefined arguments in the `args` dictionary that are there at each call:
    * `_queue` is the queue object instance in which producer should put the results;
    * `_name`  is the unique name (uuid) of this consumer instance.

An extra argument, `extra_name` is one of the arguments that we pass to the instance of the consumer ourself, as you will soon see.


Writing Consumer Function
~~~~~~~~~~~~~~~~~~~~~~~~~

Now let's write a consumer. The consumer will take one of the strings produced by the producer, and choose two verbs, one randomly and the other one from the `args` parameters; the final string will be printed to the screen. At each time, the consumer function runs, it will return how many times it's run so far.

The consumer is called as many times as many values are available for it to process plus one time after the queue is empty. This last time is there to allow any sort of clean up that the consumer might need to do.

.. code:: python

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

There are a few predefined arguments in the `args` dictionary that are there at each call:
        * `_name` is the queue object instance in which producer should put the results;
        * `_value`      -- value received from the queue to process;
        * `_last_call`  -- flag indicating that this is the last call to the
                       consumer. This can be used by the consumer to do last
                       minute clean-up work. If _last_call is True, _value is None.
        * `_result`     -- contains the return value of the previous call to the consumer
                       function. Contains None on the frst call.


Running Calculon
~~~~~~~~~~~~~~~~

Finally to put all of these together...
Start by writing a producer function. It should accept a single argument, a dictionary
of parameters passed to the function. for example:

.. code:: python

    pp = pprint.PrettyPrinter(indent=4)

    calculon = Calculon(producer,
                        [{"extra_name": "Tania"}],
                        True,
                        consumer,
                        [{"extra_action": "dances"}, {"extra_action": "sleeps"}],
                        True)

    result = calculon.start()

    pp.pprint(result)

The first and third parameters are the producer and the consumer functions,


Result
~~~~~~

.. code:: bash

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


Handling Exceptions
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    jango@sunblaze:~/workspace/calculon/calculon/example$ python example.py
    {   'consumers': [   {   'exception': ZeroDivisionError('integer division or modulo by zero',),
                             'name': 'dcf9cdbe9d8411e283ef00241dd35a03'},
                         {   'exception': ZeroDivisionError('integer division or modulo by zero',),
                             'name': 'dcfa2d2c9d8411e283ef00241dd35a03'}],
        'producers': [   {   'name': 'dcf967f29d8411e283ef00241dd35a03',
                             'result': 'Finished!'}]}


More Info
---------
The example section contains most of the functionality available through `calculon`. If you are looking for something more, dive into the :ref:`autodoc` or ask the author.


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

