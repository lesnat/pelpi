# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI

import unittest

class test_Material(unittest.TestCase):
    def setUp(self):
        self.matAl = ExampleLPI().lpiGGAl.target.material

    def tearDown(self):
        del self.matAl

    def test_electronNumberDensity(self):
        func = self.matAl.electron.number_density
        self.assertAlmostEqual(
            func().to('m**-3'),
            u.Quantity(7.830948876504127e+29, '1 / meter ** 3'))
        self.assertAlmostEqual(
            func(),
            self.matAl.ion.number_density() * self.matAl.Z(),
            delta=u.Quantity(1e-7, 'kilogram / atomic_mass_unit / meter ** 3'))

    def test_ionNumberDensity(self):
        func = self.matAl.ion.number_density
        self.assertAlmostEqual(
            func().to('m**-3'),
            u.Quantity(6.023806828080096e+28, '1 / meter ** 3'))

class test_Target(unittest.TestCase):
    def setUp(self):
        self.targAl = ExampleLPI().lpiGGAl.target

    def tearDown(self):
        del self.targAl


if __name__== '__main__':
    unittest.main()
