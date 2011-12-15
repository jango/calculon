import unittest
from calculon.calculon import Calculon

def run_test(args):
    """Runs calculon with given arguments with threading and multiprocessing
    option, returns result for both."""
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
        args = [
                   {"some_value" : "some_value", "test_id" : 1},
                   {"some_value" : "some_value", "test_id" : 1}
                 ]

        run_args = [self.producer, len(args), args, self.consumer, len(args), args]
        run_test(run_args)

    def test_return_values(self):
        args = [
                   {"test_id" : 2},
                   {"test_id" : 2}
                 ]

        run_args = [self.producer, len(args), args, self.consumer, len(args), args]
        ret_t, ret_p = run_test(run_args)

        print ret_t
       
        #print ret_p
        
        #assertEquals(ret_t["p0"], ret_t["p1"])
        #assertEquals(ret_t["c0"], ret_t["c1"])
        #assertEquals(ret_t["p0"], ret_t["p1"])
        #assertEquals(ret_t["c0"], ret_t["c1"])
        
        #    self.assertEquals(ret_t[key]["__return"], 123)

    def test_normal_t(self):
        pass
        #c_args = [
        #           {"some_value" : "some_value", "test_id" : 1},
        #           {"some_value" : "some_value", "test_id" : 1}
        #         ]
        #c = Calculon(self.producer, len(c_args), c_args,
        #             self.consumer, len(c_args), c_args)

    def test_no_param_t(self):
        pass
        #c = Calculon(self.producer, 10, None, self.consumer, 10, None)
        #c.start()
