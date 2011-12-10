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
    time.sleep(random.random() * 10)

    queue.put("--> Producer " + str(pid) + " produced: " + str(value))

def consumer(**kwargs):
    result = kwargs["_result"]
    exiting = kwargs["_exit"]
    if exiting:
        logger.info("Last call to consumer.")
    else:
        logger.info(result)
    
    # Don't forget update & return the parameters if you changed them.
    return kwargs

if __name__ == '__main__':
    P_COUNT = 100  
    C_COUNT = 100

    p_args = []
    c_args = None

    for i in range(0, P_COUNT):
        p_args.append({"value": i * 10})
    
    c = Calculon(producer, P_COUNT, p_args, consumer, C_COUNT, c_args)
    
    c.start() 
    
