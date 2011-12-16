# Calculon
This project is a customizable implementation of the producer-consumer pattern
using Python's multiprocessing & threading modules. Using the existing code you
may:

* define a custom producer and a custom consumer function;
* choose between multiprocessing or multithreading option to run the functions;
* pass arbitrary information back from each of the producer / consumer instance
back to the calling instance;

I wrote this because I needed a simple setup that would allow me to process
simple parallel computing tasks that will not benefit from a heavier approach.

# Install
To install the stable version:
    easy_install calculon
    
Otherwise, you can checkout the current code from the github repository:
https://github.com/jango/calculon

# Example
Look into **calculon-example.py** for a very simple usage example, look at the
docstings to get more info.

## Writing a producer method

    The producer method must accepts ** **kwargs **

    def producer(**kwargs):
        pid = kwargs["_pid"]
        queue = kwargs["_queue"]
        value = kwargs["value"]

        # Random delay.
        time.sleep(random.random() * 5)

        queue.put("--> Producer " + str(pid) + " produced: " + str(value))

        kwargs['__return_value'] = "p%s returns a value" % pid

        return kwargs

## Writing a consumer method
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

## Running the code:
    from calculon import Calculon

    c = Calculon(producer, P_COUNT, p_args, consumer, C_COUNT, c_args, use_threads = False)
    ret = c.start()
    print("Return values:")
    print ret

# License
This project was released under MIT license, see **LICENSE** file for more
information.

# Release Notes
See RELEASE file for the release history.
