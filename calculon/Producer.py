import uuid
import logging
from threading import Thread
from multiprocessing import Process

class _Producer:

    """Producer class."""
    def __init__(self, func, kwargs, queue, pipe):
        """Initialize new Producer.

        Keyword arguments:
        queue       -- instance of multiprocessing.Queue
        func        -- function that puts values into the queue, optional return value.
        kwargs      -- a dict of arguments passed to func.
        pipe        -- end of a Pipe()
        """

        self.name = uuid.uuid1().hex
        self.func = func
        self.kwargs = kwargs if kwargs else {}
        self.queue = queue
        self.pipe = pipe

    def run(self):
        """Runs the producer function once. Results are recorded in the
        dictionary, containing producer name and results of execution.
        Producer function has access to two arguments:
            _queue  -- the queue object where to put the results.
            __name  -- name of the producer.
        """
        # Add two additional arguments.
        self.kwargs["_name"] = self.name
        self.kwargs["_queue"] = self.queue

        self._result = self.func(self.kwargs)

        # Set result dictionary.
        self.result = {
            'name': self.name,
            'result': self._result
        }

        # For multiprocessing we need to communicate
        # results through a pipe.
        if self.pipe:
            self.pipe.send(self.result)
            self.pipe.close()


class ProducerProcess(_Producer, Process):
    """Process-based producer class."""
    def __init__(self, func, kwargs, queue, pipe):
        Process.__init__(self)
        _Producer.__init__(self, func, kwargs, queue, pipe)


class ProducerThread(_Producer, Thread):
    """Thread-based producer class."""
    def __init__(self, func, kwargs, queue):
        Thread.__init__(self)
        _Producer.__init__(self, func, kwargs, queue, None)
