#!/usr/bin/python

import time
import random
import logging
from calculon import Calculon

# Setup logging.
logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def producer(**kwargs):
    pid = kwargs["_pid"]
    queue = kwargs["_queue"]
    value = kwargs["value"]

    # Random delay.
    time.sleep(random.random() * 5)

    queue.put("--> Producer " + str(pid) + " produced: " + str(value))

    kwargs['__return_value'] = "p%s returns a value" % pid

    return kwargs

def consumer(**kwargs):
    pid = kwargs["_pid"]
    result = kwargs["_result"]
    exiting = kwargs["_exit"]

    if exiting:
        logger.info("Last call to consumer.")
        kwargs['__return_value'] = "c%s returns a value" % pid
    else:
        logger.info(result)

    return kwargs

if __name__ == '__main__':
    P_COUNT = 10
    C_COUNT = 10

    p_args = []
    c_args = None

    for i in range(0, P_COUNT):
        p_args.append({"value": i * 10})
    
    print("Running with threads...")
    c = Calculon(producer, P_COUNT, p_args, consumer, C_COUNT, c_args, use_threads = True)
    ret = c.start()
    print("Return values:")
    print ret   

    print("Running with processes...")
    c = Calculon(producer, P_COUNT, p_args, consumer, C_COUNT, c_args, use_threads = False)
    ret = c.start()
    print("Return values:")
    print ret