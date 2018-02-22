# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

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

    def test_initialize_defaults(self):
        self.po._initialize_defaults()
        self.assertEqual(self.po.default,{})
        
        self.po._initialize_defaults(input_dict={"test_input":1.0})
        self.assertEqual(self.po.default,{'test_input':1.0})
        
        self.po.test_attribute = 0.0
        self.po.test_method = self.test_check_input # instance method
        self.po._initialize_defaults(input_dict={"test_input":1.0})
        self.assertEqual(self.po.default,{'test_input':1.0,'test_method':None})
        
    def test_estimate(self):
        self.po._estimate(ExampleLPI().lpiGGAl,"Common","electron.number_total",temperature=1.0 * u.MeV, absorption_efficiency=0.1 * u(''))
        

if __name__== '__main__':
    unittest.main()
