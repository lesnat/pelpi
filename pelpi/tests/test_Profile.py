# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI,PelpiTest

import unittest

class test_Profile(PelpiTest):
    def setUp(self):
        self.sprofG = ExampleLPI().sprofG
        self.tprofG = ExampleLPI().tprofG

    def tearDown(self):
        del self.sprofG
        del self.tprofG

    def test_envelope(self):
        func = self.tprofG.envelope
        self.assertAlmostEqualQuantity(
            func(x=0*u.fs),
            1 * u(''))
        self.assertAlmostEqualQuantity(
            func(self.tprofG.fwhm()/2),
            1/2. * u(''))

    def test_integral1D(self):
        func = self.tprofG.integral1D
        self.assertAlmostEqualQuantity(
            func(),
            3.193401058293678E+01 * u.fs)

    def test_integral2D(self):
        func = self.sprofG.integral2D
        self.assertAlmostEqualQuantity(
            func(),
            1.133090035456799E+02 * u.um**2)

if __name__== '__main__':
    unittest.main()
