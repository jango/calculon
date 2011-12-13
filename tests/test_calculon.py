import unittest
from calculon.calculon import Calculon

class TestCalculon(unittest.TestCase):
    def producer(self, **kwargs):
        self.assertTrue(kwargs.has_key('_pid'))
        self.assertTrue(kwargs.has_key('_queue'))

        if kwargs.has_key("test_id"):
            test_id = kwargs["test_id"]
            # test_normal
            if test_id == 1:
                self.assertTrue(kwargs["some_value"] == "some_value")
                kwargs["_queue"].put("some_value")
                pass
        else:
            # test_no_param
            kwargs["_queue"].put(123)

    def consumer(self, **kwargs):
        self.assertTrue(kwargs.has_key('_result'))
       
        if kwargs['_result'] is None:
            self.assertTrue(kwargs.has_key('_exit'))
            self.assertTrue(kwargs['_exit'] == True)
            return kwargs
        
        if kwargs.has_key("test_id"):
            test_id = kwargs["test_id"]
            
            # test_normal
            if test_id == 1:
                print "123"
                self.assertTrue(kwargs["some_value"] == "some_value")
            else:
                # test_no_param
                print kwargs
                self.assertTrue(kwargs["_result"] == 1234)
        return kwargs

    def test_normal_p(self):
        c_args = [
                   {"some_value" : "some_value2", "test_id" : 1},
                   {"some_value" : "some_value2", "test_id" : 1}
                 ]
        c = Calculon(self.producer, len(c_args), c_args,
                     self.consumer, len(c_args), c_args, use_threads = True)
        #c.start()

    def test_no_param_p(self):
        c = Calculon(self.producer, 1, None, self.consumer, 1, None)
        c.start()
        pass

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
