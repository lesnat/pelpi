# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI

import unittest

class test_Profile(unittest.TestCase):
    def setUp(self):
        self.sprofG = ExampleLPI().lpiGGAl.laser.space_profile
        self.tprofG = ExampleLPI().lpiGGAl.laser.time_profile

    def tearDown(self):
        del self.sprofG
        del self.tprofG

    def test_timeEnvelope(self):
        func = self.tprofG.envelope
        self.assertAlmostEqual(
            func(r=0*u.fs),
            1)
        self.assertAlmostEqual(
            func(self.tprofG.fwhm()/2),
            1/2.)

    def test_spaceEnvelope(self):
        func = self.sprofG.envelope
        self.assertAlmostEqual(
            func(0*u.um),
            1)
        self.assertAlmostEqual(
            func(self.sprofG.fwhm()/2),
            1/2.)

    def test_integral1D(self):
        func = self.tprofG.integral1D
        self.assertAlmostEqual(
            func().to('fs'),
            u.Quantity(31.934010582936782, 'femtosecond'))

    def test_integral2D(self):
        func = self.sprofG.integral2D
        self.assertAlmostEqual(
            func().to('um**2'),
            u.Quantity(113.30900354567986, 'micrometer ** 2'))

if __name__== '__main__':
    unittest.main()
