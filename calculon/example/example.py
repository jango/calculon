import time
import random
import pprint
from calculon import Calculon

NAMES = ['John', 'Sally', 'Branko', 'Elena', 'Michael']
VERBS = ['walks', 'plays', 'sings', 'drinks']


def producer(args):
    for name in NAMES:
        args["_queue"].put("{0} and {1}".format(name, args["extra_name"]))

    return "Finished!"


def consumer(args):
    value = args["_value"]
    is_last_call = args["_last_call"]
    result = args["_result"]

    time.sleep(random.randint(0, 3))

    # You should never assume that the consumer instance
    # will get at least one value from the queue. If you
    # have too many consumers running, some of them can
    # get shutdown before they get a chance to process
    # a single value.
    if result is None and is_last_call:
        return 0

    # In two other cases, we just need to check if it's
    # our last cleanup call or not.
    if not is_last_call:
        print "{0} {1} and {2}.".format(value, random.choice(VERBS), args["extra_action"])

        if result is None:
            return 1
        else:
            return result + 1
    else:
        return result


pp = pprint.PrettyPrinter(indent=4)

calculon = Calculon(producer,
                    [{"extra_name": "Tania"}],
                    True,
                    consumer,
                    [{"extra_action": "dances"}, {"extra_action": "sleeps"}],
                    True)

result = calculon.start()

pp.pprint(result)
