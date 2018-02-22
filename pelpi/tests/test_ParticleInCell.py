# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI,PelpiTest

import unittest

class test_ParticleInCell(PelpiTest):
    def setUp(self):
        self.picGGAl = ExampleLPI().picGGAl

    def tearDown(self):
        del self.picGGAl

    def test_length_cell(self):
        func=self.picGGAl.length_cell
        self.assertAlmostEqualQuantity(\
        func('laser'),\
        self.picGGAl.lpi.laser.wavelength()/10)
        
        self.assertAlmostEqualQuantity(\
        func('target',temperature=1*u('MeV')),\
        2.856215138175055E-08 * u('m'))
        
        self.assertAlmostEqualQuantity(\
        min(func('laser'),func('target',temperature=1*u('MeV'))),\
        func('both',temperature=1*u('MeV')))

if __name__== '__main__':
    unittest.main()
