#!/usr/bin/python
import os
import time
import signal
import logging
from multiprocessing import Process, Queue, Event

class _Producer(Process):
    def __init__(self, logger, proc_id, queue, p, args):
        Process.__init__(self)
        self.logger = logger
        self.proc_id = proc_id
        self.args = args
        self.queue = queue
        self.p = p

    def run(self):
        if self.args is None:
            self.args = {"queue" : self.queue}
        else:
            self.args["queue"] = self.queue

        self.p(**self.args)
        
        self.logger.info("Producer instance (%s) exited..." % str(self.proc_id))


class _Consumer(Process):
    def __init__(self, logger, proc_id, queue, c, args):
        Process.__init__(self)
        self.exit = Event()

        self.logger = logger
        self.proc_id = proc_id
        self.args = args
        self.queue = queue
        self.c = c

    def run(self):
        if self.args is None:
            self.args = {"queue" : self.queue}
        else:
            self.args["queue"] = self.queue
            
        while True:
            if (self.exit.is_set() and self.queue.qsize() == 0):
                break
            else:
                try:
                    if self.queue.qsize() == 0:
                        continue
                    vals = self.queue.get(False)
                    self.args["result"] = vals
                    self.args = self.c(**self.args)
                except:
                    time.sleep(1)
                    continue
        
        self.args["exit"] = True
        self.args = self.c(**self.args)
        self.logger.info("Consumer instance (%s) exited..." % str(self.proc_id))

    def shutdown(self):
        self.logger.info("Producer (%s): instance received shutdown call..." % str(self.proc_id))
        self.exit.set()

class PC:
    def __init__(self, producer, p_count, p_args, consumer, c_count, c_args):
        if (p_args is not None and p_count != len(p_args)):
            raise ValueError("Argument count (%s) passed does not match the number of producer processes (%s)." % (str(p_count), str(len(p_args))))
    
        if (c_args is not None and c_count != len(c_args)):
            raise ValueError("Argument count (%s) passed does not match the number of consumer processes (%s)." % (str(c_count), str(len(c_args))))
        
        self.consumer = consumer
        self.c_count = c_count
        self.c_args = c_args

        self.producer = producer
        self.p_count = p_count
        self.p_args = p_args
        
        self.queue = Queue()
        
        # Setup logging.
        logging.basicConfig(format='%(asctime)-15s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
    def start(self):
        # Start producers.   
        p_procs = []
        for id in range(0, self.p_count):
            if self.p_args is None:
                p_proc = _Producer(self.logger, id, self.queue, self.producer, None)
            else:
                p_proc = _Producer(self.logger, id, self.queue, self.producer, self.p_args[id])
            p_procs.append(p_proc)
            p_proc.start()
            self.logger.info("Started Producer %s." % str(id))
    
        # Start consumers.
        c_procs = []
        for id in range(0, self.c_count):
            if self.c_args is None:
                c_proc = _Consumer(self.logger, id, self.queue, self.consumer, None)
            else:
                c_proc = _Consumer(self.logger, id, self.queue, self.consumer, c_args[id])
            c_procs.append(c_proc)
            c_proc.start()
            self.logger.info("Started Consumer %s." % str(id))
    
        # Join on the producer processes.
        for proc in p_procs:
            proc.join()            
    
        # Shut down consumers.
        for proc in c_procs:
            proc.shutdown()
    
        # Join on the consumer processes.
        for proc in c_procs:
            proc.join()