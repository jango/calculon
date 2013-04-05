import time
import uuid
import logging
from threading import Thread
from multiprocessing import Process, Event


class _Consumer:
    """Consumer class."""
    def __init__(self, func, kwargs, queue, pipe):
        """Consumer superclass, contains all of the functionality. Calculon does not deal with this
        class directly, rather it instantiates ConsumerThread or ConsumerProcess that inherit from
        _Consumer and from either Thread or Process classes.

        **Keyword arguments**

        * queue -- instance of multiprocessing.Queue;
        * func -- function that processes values received from the queue, once at a time;
        * kwargs -- a dictionary of arguments passed to func;
        * pipe -- end of a multiprocessing.Pipe() to which consumer can write the results.
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
        """Runs the producer function once.

        **Keyword arguments**

            None

        Consumer will repeteadly try to get a value from the queue until all producers have
        shutdown and the queue is not empty. Each time it succeeds, the value is passed to
        the consumer function to process the value. Once there are no more values in the
        queue and all of the producers have stopped, each of the consumers will be called
        once more, to allow to perform any sort of cleanup that might be required.

        Along with each call to the consumer function, the following values are passed in
        the argument dictionary.

        * _name -- unique name of the consumer (uuid);
        * _value -- value from the queue to process during this call;
        * _last_call -- a flag that when set to `True` indicates that this is the last "cleanup" call to the consumer. Also note that if If `_last_call` is `True`, `_value` is `None`.
        * _result -- contains the return value of the previous call to the consumer function. Set to None on the first call.
        """

        self._result = None
        self.kwargs["_result"] = None

        try:
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

                        # Special arguments get refreshed on every call.
                        self.kwargs["_name"] = self.name
                        self.kwargs["_value"] = value
                        self.kwargs["_last_call"] = False
                        self.kwargs["_result"] = self.func(self.kwargs)

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

        except Exception as e:
            self.result = {
                'name': self.name,
                'exception': e
            }

        # For multiprocessing we need to communicate results
        # through a pipe.
        if self.pipe:
            self.pipe.send(self.result)
            self.pipe.close()

    def shutdown(self):
        """Sets the exit flag. The exit flag is used by the `run()` code
        to check if the consumer can be shutdown safely. It is called from
        the Calculon instance and indicates that all of the producers have
        stopped running."""
        self.exit.set()


class ConsumerProcess(_Consumer, Process):
    """Instantiates _Consumer and Process superclasses."""
    def __init__(self, func, kwargs, queue, pipe):
        Process.__init__(self)
        _Consumer.__init__(self, func, kwargs, queue, pipe)


class ConsumerThread(_Consumer, Thread):
    """Instantiates _Consumer and Thread superclasses."""
    def __init__(self, func, kwargs, queue):
        Thread.__init__(self)
        _Consumer.__init__(self, func, kwargs, queue, None)
