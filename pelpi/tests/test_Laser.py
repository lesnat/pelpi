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
            2.354564459136066E+15 * u('1/s'))

    def test_number_density_critical(self):
        func = self.lasGG.electron.number_density_critical
        self.assertAlmostEqualQuantity(
            func(),
            1.741959882010749E+27 * u.m**-3)

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
            6.262915191331009E+13 * u.W)

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
            5.527288207777905E+23 * u('W/m**2'))

    def test_intensity_peak_normalized(self):
        func = self.lasGG.intensity_peak_normalized
        self.assertAlmostEqualQuantity(
            func(),
            5.084830087651825E+00 * u(''))
            
    def test_photon_energy(self):
        func = self.lasGG.photon.energy
        self.assertAlmostEqualQuantity(
        func(),\
        2.483057104086628E-19 * u.J)


if __name__== '__main__':
    unittest.main()
