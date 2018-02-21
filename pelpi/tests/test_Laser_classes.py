# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import numpy as np
import pelpi as pp
u=pp.unit

from examples import ExampleLPI

import unittest

class test_Laser(unittest.TestCase):
    def setUp(self):
        self.lasGG = ExampleLPI().lpiGGAl.laser

    def tearDown(self):
        del self.lasGG

    def test_envelope(self):
        func = self.lasGG.envelope
        self.assertAlmostEqual(
            func(r=0*u.m,t=0*u.fs),
            u.Quantity(1,''))
        self.assertAlmostEqual(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func(r=0*u.m,t=0*u.fs)/4)

    def test_pulsation(self):
        func = self.lasGG.pulsation
        self.assertAlmostEqual(
            func().to('s**-1'),
            u.Quantity(2354564459136066.5, '1 / second'))

    def test_numberDensityCritical(self):
        func = self.lasGG.electron.number_density_critical
        self.assertAlmostEqual(
            func().to_base_units(),
            u.Quantity(1.7419598820107494e+27, '1 / meter ** 3'))

    def test_power(self):
        func = self.lasGG.power
        self.assertAlmostEqual(
            func(),
            func(r=0*u.m,t=0*u.fs))
        self.assertAlmostEqual(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func()/4,
            delta=u.Quantity(1e-7, 'joule / femtosecond'))
        self.assertAlmostEqual(
            func().to('TW'),
            u.Quantity(62.629151913310096, 'terawatt'))

    def test_intensity(self,r=0*u('m'),t=0*u('s')):
        func = self.lasGG.intensity
        self.assertAlmostEqual(
            func(),
            func(r=0*u.m,t=0*u.fs))
        self.assertAlmostEqual(
            func(t = self.lasGG.time_profile.fwhm()/2,r = self.lasGG.space_profile.fwhm()/2),
            func()/4,
            delta=u.Quantity(1e-7, 'joule / femtosecond / micrometer ** 2'))
        self.assertAlmostEqual(
            func().to('W/cm**2'),
            u.Quantity(5.527288207777904e+19, 'watt / centimeter ** 2'))

    def test_intensityNormalized(self):
        func = self.lasGG.intensity_peak_normalized
        self.assertAlmostEqual(
            func(),
            u.Quantity(5.055509932021204, 'dimensionless'))

    # def test_timeChirp(self):
    #     func = self.lasGG.time_chirp
    #     self.assertAlmostEqual(
    #         func(t=0*u.fs),
    #         func(t=0*u.fs,phase=u.Quantity(2*np.pi)))
    #     self.assertAlmostEqual(
    #         func(t=0*u.fs),
    #         0)


if __name__== '__main__':
    unittest.main()
