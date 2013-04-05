import uuid
import logging
from threading import Thread
from multiprocessing import Process

class _Producer:

    """Producer class."""
    def __init__(self, func, kwargs, queue, pipe):
        """Producer superclass, contains all of the functionality. Calculon does not deal with this
        class directly, rather it instantiates ProducerThread or ProducerProcess that inherit from
        _Producer and from either Thread or Process classes.

        **Keyword arguments**

        * queue -- instance of multiprocessing.Queue;
        * func -- function that puts values into the queue, optional return value;
        * kwargs -- a dictionary of arguments passed to func;
        * pipe -- end of a multiprocessing.Pipe() to which producer can write the results.
        """

        self.name = uuid.uuid1().hex
        self.func = func
        self.kwargs = kwargs if kwargs else {}
        self.queue = queue
        self.pipe = pipe

    def run(self):
        """Runs the producer function once.

        **Keyword arguments**

            None

        When the producer function is called, two additional arguments are passed to it:

        * _name -- unique name of the producer (uuid);
        * _queue -- the queue object where to put the results;.

        **Returns**

        * If the run completed successfully, the method returns a dictionary with two keys:

            * "name" -- name of this producer (uuid);
            * "result" -- the return value returned from the producer function.

        * If the run completed unsuccessfully, the method returns a dictionary with two keys:

            * "name" -- name of this producer (uuid);
            * "exception" -- the exception object for the raised exception.
        """
        # Add two additional arguments.
        self.kwargs["_name"] = self.name
        self.kwargs["_queue"] = self.queue

        try:
            self._result = self.func(self.kwargs)

            # Set result dictionary.
            self.result = {
                'name': self.name,
                'result': self._result
            }
        except Exception as e:
            self.result = {
                'name': self.name,
                'exception': e
            }

        # For multiprocessing we need to communicate results through a pipe.
        if self.pipe:
            self.pipe.send(self.result)
            self.pipe.close()


class ProducerProcess(_Producer, Process):
    """Process-based producer class."""
    def __init__(self, func, kwargs, queue, pipe):
        """Instantiates _Producer and Process superclasses."""
        Process.__init__(self)
        _Producer.__init__(self, func, kwargs, queue, pipe)


class ProducerThread(_Producer, Thread):
    """Thread-based producer class."""
    def __init__(self, func, kwargs, queue):
        """Instantiates _Producer and Thread superclasses."""
        Thread.__init__(self)
        _Producer.__init__(self, func, kwargs, queue, None)
