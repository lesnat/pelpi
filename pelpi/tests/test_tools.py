# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

_Default = pp._tools._Default

from examples import ExampleLPI

import unittest

class test_PelpiObject(unittest.TestCase):
    def setUp(self):
        self.po = pp._tools._PelpiObject()
    
    def tearDown(self):
        del self.po
        
    def test_check_input(self):
        self.po._check_input('int',1,int)
        self.po._check_input('float',1.0,float)
        self.po._check_input('str','test',str)
        self.po._check_input('float',1.0,"<type 'float'>")
    """
    def test_estimate(self):
        self.po._estimate(ExampleLPI().lpiGGAl,"Common","electron.number_total",temperature=1.0 * u.MeV, efficiency_absorption=0.1 * u(''))
    """ 
        
class test_Default(unittest.TestCase):
    def setUp(self):
        self.empty = Empty()

    def tearDown(self):
        del self.empty

    def test_initialize_defaults(self):
        self.empty.default = _Default(self.empty)
        self.assertEqual(self.empty.default.get(key='all'),{})
        
        self.empty.default = _Default(self.empty,input_dict={"test_input":1.0})
        self.assertEqual(self.empty.default.get(key='all'),{'test_input':1.0})
        
        self.empty.test_attribute = 0.0
        self.empty.test_method = self.setUp # instance method
        self.empty.default = _Default(self.empty,input_dict={"test_input":1.0})
        self.assertEqual(self.empty.default.get(key='all'),{'test_input':1.0,'test_method':None})
        
class Empty():
    """
    Empty class, for testing defaults.
    Otherwise it takes unittest.TestCase instance methods as default dict entries.
    """
    pass

if __name__== '__main__':
    unittest.main()
