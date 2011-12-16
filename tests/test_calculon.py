import unittest
from calculon import Calculon

def run_test(args):
    """Runs calculon with given arguments with both threading and
    multiprocessing option and returns result for both."""
    c = Calculon(*args, use_threads = True)
    ret_t = c.start()

    c = Calculon(*args, use_threads = False)
    ret_p = c.start()
    
    return ret_t, ret_p

class TestCalculon(unittest.TestCase):
    def producer(self, **kwargs):
        self.assertTrue(kwargs.has_key('_pid'))
        self.assertTrue(kwargs.has_key('_queue'))

        if kwargs.has_key("test_id"):
            test_id = kwargs["test_id"]
            # test_normal_run
            if test_id == 1:
                self.assertTrue(kwargs["some_value"] == "some_value")
                kwargs["_queue"].put("some_value")
            elif test_id == 2:
                kwargs["_queue"].put(123)
                if kwargs.has_key('__produced'):
                    kwargs['__produced'] += 1
                else:
                    kwargs['__produced'] = 1                
        else:
            # test_no_params
            kwargs["_queue"].put(123)
            
        return kwargs

    def consumer(self, **kwargs):
        self.assertTrue(kwargs.has_key('_result'))
       
        if kwargs['_result'] is None:
            self.assertTrue(kwargs.has_key('_exit'))
            self.assertTrue(kwargs['_exit'] == True)
            return kwargs
        
        if kwargs.has_key("test_id"):
            test_id = kwargs["test_id"]
            
            # test_normal_run
            if test_id == 1:
                self.assertTrue(kwargs["some_value"] == "some_value")
            elif test_id == 2:
                if kwargs.has_key('__consumed'):
                    kwargs['__consumed'] += 1
                else:
                    kwargs['__consumed'] = 1
        else:
            # test_no_params
            self.assertTrue(kwargs["_result"] == 123)
        return kwargs
      
    def test_no_params(self):
        """Testing running with no parameters."""
        c_args = None
        
        run_args = [self.producer, 0, c_args, self.consumer, 0, c_args]
        run_test(run_args)

    def test_normal_run(self):
        """Testing passing values to initialize producer and consumer receiving
        values from the queue."""
        args = [{"some_value" : "some_value", "test_id" : 1}] 
        run_args = [self.producer, len(args), args, self.consumer, len(args), args]
        run_test(run_args)

    def test_return_values(self):
        """Testing the ability to return values. Consumer/Producer return number
        of values consumed/produced. Since consumer might have uneven
        distribution of the number of consumed values, doing a summation
        instead. In addition, the result for thread and process run should
        match."""

        args = [{"test_id" : 2} for n in range(2)] 
        run_args = [self.producer, len(args), args, self.consumer, len(args), args]
        ret_t, ret_p = run_test(run_args)

        t_sum = [0, 0]
        p_sum = [0, 0]
        for id in range(0, len(args)):
            p_key = "p" + str(id)
            c_key = "c" + str(id)

            t_sum[0] += ret_t[p_key].get("__produced", 0)
            t_sum[1] += ret_t[c_key].get("__consumed", 0)

            p_sum[0] += ret_p[p_key].get("__produced", 0)
            p_sum[1] += ret_p[c_key].get("__consumed", 0)

        self.assertEquals(t_sum[0], len(args))
        self.assertEquals(t_sum[0], t_sum[1])
        self.assertEquals(p_sum[0], t_sum[0])
        self.assertEquals(p_sum[1], t_sum[1])
