import random
import unittest
from multiprocessing import Queue, Pipe

from calculon import Calculon
from calculon import ProducerProcess, ProducerThread
from calculon import ConsumerProcess, ConsumerThread

NUM_RESULTS = 5


def prod_function(kwargs):
    """Producer function that generates random integers.
    It returns a list of generated integers plus an
    integer passed to it vis kwargs['add']"""

    # Check the name is available.
    kwargs['_name']

    queue = kwargs['_queue']
    add = kwargs['add']

    values = []
    for i in range(0, NUM_RESULTS):
        value = random.randint(1, 10)
        values.append(value)
        queue.put(value)

    values.append(int(add))

    return values


def cons_function(kwargs):
    """Consumer function gets integers from the queue and
    stores them in a list passed throughout the calls.
    At the last call, the list plus the kwargs['add'] is
    returned."""

    kwargs['_name']
    is_last_call = kwargs['_last_call']
    add = kwargs['add']
    value = kwargs['_value']
    result = kwargs['_result']

    # If our first call was our last call.
    if result is None and is_last_call:
        return [add]

    # Otherwise, if it's not our last call.
    if not is_last_call:
        if result is None:
            int_list = [value]
        else:
            int_list = result + [value]
    # And if it is.
    else:
        int_list = result + [int(add)]

    return int_list


class TestCalculon(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()
        self.pipe = Pipe()

    def test_producer_thread(self):
        """Check producer by itself, running as a thread."""
        pt = ProducerThread(prod_function, {'add': 5}, self.queue)
        pt.start()
        pt.join()

        # The queue is the correct size.
        self.assertTrue(self.queue.qsize() == NUM_RESULTS)

        # All of the results are in the range.
        while self.queue.qsize() > 0:
            result = self.queue.get()
            self.assertTrue(result in range(1, 11))

        # Producer's range is NUM_RESULTS + 1 (add variable).
        self.assertTrue(len(pt.result["result"]) == NUM_RESULTS + 1)

    def test_producer_process(self):
        """Check producer by itself, running as a process."""
        pp = ProducerProcess(prod_function, {'add': 5}, self.queue, self.pipe[0])
        pp.start()
        pp.join()

        # The queue is the correct size.
        self.assertTrue(self.queue.qsize() == NUM_RESULTS)

        # All of the results are in the range.
        while self.queue.qsize() > 0:
            result = self.queue.get()
            self.assertTrue(result in range(1, 11))

        # Producer's range is NUM_RESULTS + 1 (add variable).
        self.assertTrue(len(self.pipe[1].recv()["result"]) == NUM_RESULTS + 1)

    def test_consumer_thread(self):
        """Check consumer by itself, running as a thread."""
        for i in range(0, NUM_RESULTS):
            self.queue.put(i)

        ct = ConsumerThread(cons_function, {'add': 5}, self.queue)
        ct.start()
        ct.shutdown()
        ct.join()

        # The queue is empty, the results contain all numbers.
        self.assertTrue(self.queue.qsize() == 0)
        self.assertTrue(len(ct.result["result"]) == NUM_RESULTS + 1)

        # All result values are in correct range.
        for value in ct.result["result"]:
            self.assertTrue(str(value), value in range(1, 11))

    def test_consumer_process(self):
        """Check consumer by itself, running as a process."""
        for i in range(0, NUM_RESULTS):
            self.queue.put(i)

        cp = ConsumerProcess(cons_function, {'add': 5}, self.queue, self.pipe[0])
        cp.start()
        cp.shutdown()
        cp.join()

        result = self.pipe[1].recv()["result"]

        # The queue is empty, the results contain all numbers.
        self.assertTrue(self.queue.qsize() == 0)
        self.assertTrue(len(result) == NUM_RESULTS + 1)

        # All result values are in correct range.
        for value in result:
            self.assertTrue(str(value), value in range(1, 11))

    def test_calculon_thread(self):
        """The four Calculon tests check that we can run calculon as thread/process/combination.
        The idea is to generate random numbers in producer, retrieve them through consumer,
        add up the result and compare the two."""
        NUM_PROD = 50
        NUM_CONS = 30

        p_args = []
        c_args = []

        for i in range(NUM_PROD):
            p_args.append({"add": 0})

        for i in range(NUM_CONS):
            c_args.append({"add": 0})

        c = Calculon(prod_function, p_args, True, cons_function, c_args, True)
        result = c.start()

        prod_sum = 0
        cons_sum = 0

        for p in result["producers"]:
            prod_sum += sum(p["result"])

        for c in result["consumers"]:
            cons_sum += sum(c["result"])

        self.assertTrue(prod_sum == cons_sum)

    def test_calculon_process(self):
        NUM_PROD = 50
        NUM_CONS = 30

        p_args = []
        c_args = []

        for i in range(NUM_PROD):
            p_args.append({"add": 0})

        for i in range(NUM_CONS):
            c_args.append({"add": 0})

        c = Calculon(prod_function, p_args, False, cons_function, c_args, False)
        result = c.start()

        prod_sum = 0
        cons_sum = 0

        for p in result["producers"]:
            prod_sum += sum(p["result"])

        for c in result["consumers"]:
            cons_sum += sum(c["result"])

        self.assertTrue(prod_sum == cons_sum)

    def test_calculon_hybrid_1(self):
        NUM_PROD = 50
        NUM_CONS = 30

        p_args = []
        c_args = []

        for i in range(NUM_PROD):
            p_args.append({"add": 0})

        for i in range(NUM_CONS):
            c_args.append({"add": 0})

        c = Calculon(prod_function, p_args, True, cons_function, c_args, False)
        result = c.start()

        prod_sum = 0
        cons_sum = 0

        for p in result["producers"]:
            prod_sum += sum(p["result"])

        for c in result["consumers"]:
            cons_sum += sum(c["result"])

        self.assertTrue(prod_sum == cons_sum)

    def test_calculon_hybrid_2(self):
        NUM_PROD = 50
        NUM_CONS = 30

        p_args = []
        c_args = []

        for i in range(NUM_PROD):
            p_args.append({"add": 0})

        for i in range(NUM_CONS):
            c_args.append({"add": 0})

        c = Calculon(prod_function, p_args, False, cons_function, c_args, True)
        result = c.start()

        prod_sum = 0
        cons_sum = 0

        for p in result["producers"]:
            prod_sum += sum(p["result"])

        for c in result["consumers"]:
            cons_sum += sum(c["result"])

        self.assertTrue(prod_sum == cons_sum)

    def test_exceptions(self):
        """Checks that exceptions don't kill Calculon"""
        NUM_PROD = 1
        NUM_CONS = 1

        p_args = []
        c_args = []

        for i in range(NUM_PROD):
            p_args.append({"add": None})

        for i in range(NUM_CONS):
            c_args.append({"add": None})

        c = Calculon(prod_function, p_args, False, cons_function, c_args, True)
        result = c.start()

if __name__ == '__main__':
    unittest.main()
