import time
from multiprocessing import Process, Queue, Event

class Calculon:
    """Producer-consumer class. Resonsible for initializing producer
    and consumer classes and controls execution."""
    def __init__(self, producer, p_count, p_args, consumer, c_count, c_args):
        """Initialize Calculon object.

        Keyword arguments:
        producer    -- producer function that accepts **kwargs
        p_count     -- number of producer processes
        p_args      -- list of {}, specifying arguments for the producer
                       processes, the size of list must either match p_count or
                       be None
        consumer    -- consumer function that accepts **kwargs
        c_count     -- consumer of producer processes
                       size of list must either match p_count or be None
        c_args      -- list of {}, specifying arguments for the consumer
                       processes, the size of list must either match p_count or
                       be None

        """        
        
        # Make sure that # arguments matches # of processes or is None.
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

        # Initialize the Queue.        
        self.queue = Queue()
        
    def start(self):
        """Starts producer and consumer processes and controls the shutdown."""

        # Start producers.   
        p_procs = []
        for id in range(0, self.p_count):
            if self.p_args is None:
                p_proc = _Producer(id, self.queue, self.producer, None)
            else:
                p_proc = _Producer(id, self.queue, self.producer, self.p_args[id])
            p_procs.append(p_proc)
            p_proc.start()
    
        # Start consumers.
        c_procs = []
        for id in range(0, self.c_count):
            if self.c_args is None:
                c_proc = _Consumer(id, self.queue, self.consumer, None)
            else:
                c_proc = _Consumer(id, self.queue, self.consumer, c_args[id])
            c_procs.append(c_proc)
            c_proc.start()
   
        # Join on the producer processes.
        for proc in p_procs:
            proc.join()            
    
        # Shut down consumers.
        for proc in c_procs:
            proc.shutdown()
    
        # Join on the consumer processes.
        for proc in c_procs:
            proc.join()

class _Producer(Process):
    """Producer class."""
    def __init__(self, proc_id, queue, p, args):
        """Initialize Producer object.

        Keyword arguments:
        logger  -- shared logging instance
        proc_id -- id of the producer process 
        queue   -- shared queue
        p       -- producer function
        args    -- a {} of arguments to be passed to the producer function

        """

        Process.__init__(self)
        self.proc_id = proc_id
        self.queue = queue
        self.p = p
        self.args = args

    def run(self):
        """Runs the producer function once. All of the arguments in self.args
        are passed to the function, in addition to two internal ones:

        _queue -- shared queue
        _pid -- id of the producer process

        """

        if self.args is None: self.args = {}

        # Internal args.
        self.args["_queue"] = self.queue
        self.args["_pid"] = self.proc_id 

        self.p(**self.args)

class _Consumer(Process):
    """Consumer class."""
    def __init__(self, proc_id, queue, c, args):
        """Initialize Producer object.

        Keyword arguments:
        proc_id -- id of the consumer process 
        queue   -- shared queue
        c       -- consumer function
        args    -- a {} of arguments to be passed to the producer function

        """
        Process.__init__(self)
        # Exit event indicating that there will be no items produced and it's
        # safe to exit once queue is empty.
        self.exit = Event()
        self.proc_id = proc_id
        self.args = args
        self.queue = queue
        self.c = c

    def run(self):
        """Runs the consumer function. All of the arguments in self.args are
        passed to the function, in addition to two internal ones:

        _pid    -- id of the consumer process
        _result -- value received from the queue
        _exit   -- flag indicating that this is the last (clean-up) call to the
                   consumer. This can be used by the consumer to do some last
                   minute clean-up work. If _exit is True, _result is None.

        Everytime the consumer is called (until the exit flag is set to true
        and there are no more items left in the queue) it's return value will
        be fed to itself on the next iteration so that the function can persist
        values if needed.
        """

        # Internal args.
        if self.args is None: self.args = {}

        self.args["_pid"] = self.proc_id
        self.args["_result"] = None
        self.args["_exit"] = False
            
        while not (self.exit.is_set() and self.queue.qsize() == 0):
            try:
                vals = self.queue.get(False)
                self.args["_result"] = vals
                self.args = self.c(**self.args)
            except:
                time.sleep(1)
                continue

        # Last iteration call.        
        self.args["_exit"] = True
        self.args["_result"] = None

        self.args = self.c(**self.args)

    def shutdown(self):
        self.exit.set()

