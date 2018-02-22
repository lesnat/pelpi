# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI,PelpiTest

import unittest

class test_Material(PelpiTest):
    def setUp(self):
        self.matAl = ExampleLPI().matAl

    def tearDown(self):
        del self.matAl

    def test_electron_number_density(self):
        func = self.matAl.electron.number_density
        self.assertAlmostEqualQuantity(
            func(),
            7.830948876504127E+29 * u.m**-3)
            
        self.assertAlmostEqualQuantity(
            func(),
            self.matAl.ion.number_density() * self.matAl.Z())

    def test_ion_number_density(self):
        func = self.matAl.ion.number_density
        self.assertAlmostEqual(
            func().to('m**-3'),
            6.023806828080096E+28 * u.m**-3)



if __name__== '__main__':
    unittest.main()
