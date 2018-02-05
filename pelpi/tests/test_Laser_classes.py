# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import numpy as np
import pelpi as pp
u=pp.unit

import unittest

class test_Profile(unittest.TestCase):
    def setUp(self):
        self.profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u('fs'),
            space_profile   = "gaussian",
            space_fwhm      = 10*u('um'),)

    def tearDown(self):
        del self.profGG

    def test_instanciate(self): # TODO: implement other profiles
        # Gaussian + Gaussian profile
        self.profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u('fs'),
            space_profile   = "gaussian",
            space_fwhm      = 10*u('um'),)
        self.assertEqual(self.profGG.time_profile() , "gaussian")
        self.assertEqual(self.profGG.time_fwhm()    , 30*u('fs'))
        self.assertEqual(self.profGG.space_profile(), "gaussian")
        self.assertEqual(self.profGG.space_fwhm()   , 10*u('um'))

        # tatatata + Super-gaussian profile
        # self.profTSg =

        # tatata + Top-hat profile
        # self.profTTh
        # self.assertEqual(self.profGG.space_radius , self.space_radius)

        # test with wrong units
        # test with wrong profile name
        # test with uncomplete informations on kwargs

    def test_timeEnvelope(self):
        func = self.profGG.timeEnvelope
        self.assertAlmostEqual(
            func(t=0*u.fs),
            1)
        self.assertAlmostEqual(
            func(self.profGG.time_fwhm()/2),
            1/2.)

    def test_spaceEnvelope(self):
        func = self.profGG.spaceEnvelope
        self.assertAlmostEqual(
            func(0*u.um),
            1)
        self.assertAlmostEqual(
            func(self.profGG.space_fwhm()/2),
            1/2.)

    def test_envelope(self):
        func = self.profGG.envelope
        self.assertAlmostEqual(
            func(r=0*u.m,t=0*u.fs),
            u.Quantity(1,''))
        self.assertAlmostEqual(
            func(t = self.profGG.time_fwhm()/2,r = self.profGG.space_fwhm()/2),
            func(r=0*u.m,t=0*u.fs)/4)

    def test_timeIntegral(self):
        func = self.profGG.timeIntegral
        self.assertAlmostEqual(
            func().to('fs'),
            u.Quantity(31.934010582936782, 'femtosecond'))

    def test_spaceIntegralDouble(self):
        func = self.profGG.spaceIntegralDouble
        self.assertAlmostEqual(
            func().to('um**2'),
            u.Quantity(113.30900354567986, 'micrometer ** 2'))


class test_Laser(unittest.TestCase):
    def setUp(self):
        profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u.fs,
            space_profile   = "gaussian",
            space_fwhm      = 10*u.um)

        self.lasGG=pp.Laser(
            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            Profile    = profGG,

            # contrast_1ps = 1e8,
            #
            # polarization = [0,1,0],
            #
            # direction  = [0,0,1],
            # angle      = 0. * u.deg,
            )

    def tearDown(self):
        del self.lasGG

    def test_instanciate(self): # TODO: implement other profiles
        # Gaussian + Gaussian profile
        profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u.fs,
            space_profile   = "gaussian",
            space_fwhm      = 10*u.um)

        self.lasGG=pp.Laser(
            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            Profile    = profGG,

            # contrast_1ps = 1e8,
            #
            # polarization = [0,1,0],
            #
            # direction  = [0,0,1],
            # angle      = 0. * u.deg,
            )

        self.assertEqual(self.lasGG.wavelength()  , 0.8 * u.um)
        self.assertEqual(self.lasGG.energy()      , 2.0 * u.J)
        self.assertEqual(self.lasGG.profile     , profGG)
        # self.assertEqual(self.lasGG.contrast_1ps, 1e8)
        # self.assertEqual(self.lasGG.polarization, [0,1,0])
        # self.assertEqual(self.lasGG.direction   , [0,0,1])
        # self.assertEqual(self.lasGG.angle       , 0. * u.deg)

        # tatata + Super-gaussian profile
        # ...


    def test_pulsation(self):
        func = self.lasGG.pulsation
        self.assertAlmostEqual(
            func().to('s**-1'),
            u.Quantity(2354564459136066.5, '1 / second'))

    def test_numberDensityCritical(self):
        func = self.lasGG.numberDensityCritical
        self.assertAlmostEqual(
            func().to_base_units(),
            u.Quantity(1.7419598820107494e+27, '1 / meter ** 3'))

    def test_power(self):
        func = self.lasGG.power
        self.assertAlmostEqual(
            func(),
            func(r=0*u.m,t=0*u.fs))
        self.assertAlmostEqual(
            func(t = self.lasGG.profile.time_fwhm()/2,r = self.lasGG.profile.space_fwhm()/2),
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
            func(t = self.lasGG.profile.time_fwhm()/2,r = self.lasGG.profile.space_fwhm()/2),
            func()/4,
            delta=u.Quantity(1e-7, 'joule / femtosecond / micrometer ** 2'))
        self.assertAlmostEqual(
            func().to('W/cm**2'),
            u.Quantity(5.527288207777904e+19, 'watt / centimeter ** 2'))

    def test_intensityNormalized(self):
        func = self.lasGG.intensityPeakNormalized
        self.assertAlmostEqual(
            func(),
            u.Quantity(5.055509932021204, 'dimensionless'))

    def test_timeChirp(self):
        func = self.lasGG.timeChirp
        self.assertAlmostEqual(
            func(t=0*u.fs),
            func(t=0*u.fs,phase=u.Quantity(2*np.pi)))
        self.assertAlmostEqual(
            func(t=0*u.fs),
            0)


if __name__== '__main__':
    unittest.main()
