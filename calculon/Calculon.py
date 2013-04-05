from multiprocessing import Queue, Pipe

from Consumer import ConsumerProcess, ConsumerThread
from Producer import ProducerProcess, ProducerThread


class Calculon:
    """Producer-consumer class. Responsible for initializing producers and consumers and controlling execution."""
    def __init__(self, prod_func, prod_kwargs, prod_use_threads, cons_func, cons_kwargs, cons_use_threads):
        """Initializes Calculon.

        **Keyword arguments**

        * prod_func    -- producer function that accepts one argument (dictionary of values);
        * prod_kwargs  -- a list of dictionaries, each representing a set of arguments for an instance of the producer function;
        * prod_use_threads -- a flag specifying if threads are used to run producer code (if False, processes are used);
        * cons_func    -- consumer function that accepts one argument (dictionary of values)
        * cons_kwargs  -- a list of dictionaries, each representing a set of arguments for an instance of the consumer function
        * cons_use_threads -- a flag specifying if threads are used to run consumer code (if False, processes are used).
        """

        self.cons_func = cons_func
        self.cons_kwargs = cons_kwargs
        self.cons_use_threads = cons_use_threads

        self.prod_func = prod_func
        self.prod_kwargs = prod_kwargs
        self.prod_use_threads = prod_use_threads

        self.queue = Queue()

    def start(self):
        """Starts producer and consumer threads / processes and controls the execution.

        **Keyword arguments**

            None

        **Returns**
            Returns a dictionary containing two elements:

            * value for key "producers" contains a list of results returned by each of the producer instance.
            * value for key "consumers" contains a list of results returned by each of the consumer instance.
        """

        # Producers.
        prod_objs = []
        prod_pipes = []

        for id in range(0, len(self.prod_kwargs)):
            args = self.prod_kwargs[id]

            if self.prod_use_threads:
                prod_obj = ProducerThread(self.prod_func, args, self.queue)
            else:
                prod_pipes.append(Pipe())
                prod_obj = ProducerProcess(self.prod_func, args, self.queue, prod_pipes[id][0])

            prod_objs.append(prod_obj)
            prod_obj.start()

        # Consumers.
        cons_objs = []
        cons_pipes = []

        for id in range(0, len(self.cons_kwargs)):
            args = self.cons_kwargs[id]

            if self.cons_use_threads:
                cons_obj = ConsumerThread(self.cons_func, args, self.queue)
            else:
                cons_pipes.append(Pipe())
                cons_obj = ConsumerProcess(self.cons_func, args, self.queue, cons_pipes[id][0])

            cons_objs.append(cons_obj)
            cons_obj.start()

        # Join on the producers.
        for prod_obj in prod_objs:
            prod_obj.join()

        # Shut down  theconsumers.
        for cons_obj in cons_objs:
            cons_obj.shutdown()

        # Join on the consumers.
        for cons_obj in cons_objs:
            cons_obj.join()

        # Collect result values.
        result = {"producers": [],
                  "consumers": []}

        for counter, prod_obj in enumerate(prod_objs):
            if isinstance(prod_obj, ProducerProcess):
                res = prod_pipes[counter][1].recv()
            else:
                res = prod_obj.result

            result["producers"] = result["producers"] + [res]

        for counter, cons_obj in enumerate(cons_objs):
            if isinstance(cons_obj, ConsumerProcess):
                res = cons_pipes[counter][1].recv()
            else:
                res = cons_obj.result

            result["consumers"] = result["consumers"] + [res]

        return result
