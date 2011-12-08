import logging
from pc import PC

# Setup logging.
logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def producer(**kwargs):
    kwargs["queue"].put(str(kwargs["id"]) + " produces " + str(kwargs["value"]))
    return

def consumer(**kwargs):
    result = kwargs["result"]
    exiting = kwargs["exit"]
    
    if exiting:
        logger.info("Last call to consumer.")
    else:
        logger.info(result)
    
    # Don't forget the parameters if you changed them.
    return kwargs

if __name__ == '__main__':
    
    p_args = [
        {"id": 0, "value": 10},
        {"id": 1, "value": 20},
        {"id": 2, "value": 30},
        {"id": 3, "value": 40},
        {"id": 4, "value": 50},      
    ]
    
    c_args = None
    
    pc = PC(producer, 5, p_args, consumer, 5, c_args)
    
    pc.start() 
    