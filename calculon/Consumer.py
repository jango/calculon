import time
import uuid
import logging
from threading import Thread
from multiprocessing import Process, Event


class _Consumer:
    """Consumer class."""
    def __init__(self, func, kwargs, queue, pipe):
        """Initialize Consumer object.

        Keyword arguments:
        func        -- function that puts values into the queue, optional return value.
        kwargs      -- a dict of arguments passed to func.
        queue       -- instance of multiprocessing.Queue
        pipe        -- end of a Pipe()
        """

        self.name = uuid.uuid1().hex
        self.func = func
        self.kwargs = kwargs if kwargs else {}
        self.queue = queue
        self.pipe = pipe

        # Exit event indicating that there will be no items out on the queue
        # anymore and that it's safe to exit once queue is empty.
        self.exit = Event()

    def run(self):
        """Runs the consumer function. All of the arguments in self.args are
        passed to the function, in addition to four internal ones:

        _name       -- id of the consumer process;
        _value      -- value received from the queue to process;
        _last_call  -- flag indicating that this is the last call to the
                       consumer. This can be used by the consumer to do last
                       minute clean-up work. If _last_call is True, _value is None.
        _result     -- contains the return value of the previous call to the consumer
                       function. Contains None on the frst call.
        """

        self._result = None
        self.kwargs["_result"] = None

        while not (self.exit.is_set() and self.queue.qsize() == 0):
            # Value to process.
            value = None

            # We use a non-blocking call to avoid deadlocking when
            # the queue is empty.
            try:
                value = self.queue.get(block=False)
            except:
                time.sleep(1)
                continue

            if value is not None:
                try:
                    # Special arguments get refreshed on every call.
                    self.kwargs["_name"] = self.name
                    self.kwargs["_value"] = value
                    self.kwargs["_last_call"] = False
                    self.kwargs["_result"] = self.func(self.kwargs)
                except Exception as e:
                    logging.error("Consumer '{0}' could not consume '{1}'".format(self.name, self.kwargs))
                    logging.exception(e)

        # Last call to the consumer.
        self.kwargs["_name"] = self.name
        self.kwargs["_value"] = None
        self.kwargs["_last_call"] = True
        self._result = self.func(self.kwargs)

        # Set result dictionary.
        self.result = {
            'name': self.name,
            'result': self._result
        }

        # For multiprocessing we need to communicate results
        # through a pipe.
        if self.pipe:
            self.pipe.send(self.result)
            self.pipe.close()

    def shutdown(self):
        """Sets exit flag."""
        self.exit.set()


class ConsumerProcess(_Consumer, Process):
    """Process-based consumer class."""
    def __init__(self, func, kwargs, queue, pipe):
        Process.__init__(self)
        _Consumer.__init__(self, func, kwargs, queue, pipe)


class ConsumerThread(_Consumer, Thread):
    """Thread-based consumer class."""
    def __init__(self, func, kwargs, queue):
        Thread.__init__(self)
        _Consumer.__init__(self, func, kwargs, queue, None)
