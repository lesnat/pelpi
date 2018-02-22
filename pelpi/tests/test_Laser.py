# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import numpy as np
import pelpi as pp
u=pp.unit

from examples import ExampleLPI,PelpiTest

import unittest

class test_Laser(PelpiTest):
    def setUp(self):
        self.lasGG = ExampleLPI().lasGG

    def tearDown(self):
        del self.lasGG

    def test_envelope(self):
        func = self.lasGG.envelope
        self.assertAlmostEqualQuantity(
            func(r=0*u.m,t=0*u.fs),
            1 *u(''))
        self.assertAlmostEqualQuantity(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func(r=0*u.m,t=0*u.fs)/4)

    def test_angular_frequency(self):
        func = self.lasGG.angular_frequency
        self.assertAlmostEqualQuantity(
            func(),
            2354564459136066.5 * u('1/s'))

    def test_number_density_critical(self):
        func = self.lasGG.electron.number_density_critical
        self.assertAlmostEqualQuantity(
            func(),
            1.7419598820107494e+27 * u.m**-3)

    def test_power(self):
        func = self.lasGG.power
        self.assertAlmostEqualQuantity(
            func(),
            func(r=0*u.m,t=0*u.fs))
        self.assertAlmostEqualQuantity(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func()/4)
        self.assertAlmostEqualQuantity(
            func(),
            62.629151913310096 * u.TW)

    def test_intensity(self,r=0*u('m'),t=0*u('s')):
        func = self.lasGG.intensity
        self.assertAlmostEqualQuantity(
            func(),
            func(r=0*u.m,t=0*u.fs))
        self.assertAlmostEqualQuantity(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func()/4)
        self.assertAlmostEqualQuantity(
            func(),
            5.527288207777904e+19 * u('W/cm**2'))

    def test_intensity_peak_normalized(self):
        func = self.lasGG.intensity_peak_normalized
        self.assertAlmostEqualQuantity(
            func(),
            5.055509932021204 * u(''))


if __name__== '__main__':
    unittest.main()
