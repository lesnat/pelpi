#coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)
import pelpi as pp
u=pp.unit

__all__=['ExampleLPI']

class ExampleLPI(object):
    """
    Class with different LaserPlasmaInteraction objects instanciated,
    for shorten setUp methods.
    """
    def __init__(self):
        self.tprofG = pp.Profile(
            profile    = "gaussian1D",
            fwhm       = 30*u.fs,
        )
        self.sprofG = pp.Profile(
            profile    = "gaussian2D",
            fwhm       = 10*u.um,
        )
        self.lasGG=pp.Laser(
            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            time_profile    = self.tprofG,
            space_profile   = self.sprofG,
        )
        self.matAl  = pp.Material(
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u('amu'),
            Z           = 13 * u(''),
        )

        self.targAl = pp.Target(self.matAl)

        self.lpiGGAl = pp.LaserPlasmaInteraction(self.lasGG,self.targAl)
        
        
import unittest

class PelpiTest(unittest.TestCase):
    relative_precision=1e-7 # Class attribute, for all tests
        
    def assertAlmostEqualQuantity(self,Q1,Q2): # try except for giving more detailled result
        q1 = Q1.to_base_units()
        q2 = Q2.to_base_units()
        self.assertEqual(q1.units,q2.units)
        if q1.magnitude!=0.0:
            relative_difference = abs(q1.magnitude-q2.magnitude)/q1.magnitude
        elif q2.magnitude!=0.0:
            relative_difference = abs(q1.magnitude-q2.magnitude)/q1.magnitude
        else:
            relative_difference = 0.0 # both magnitudes = 0.0
        self.assertAlmostEqual(relative_difference,0.0,delta=self.relative_precision)
