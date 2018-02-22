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
        tprofG = pp.Profile(
            profile    = "gaussian1D",
            fwhm       = 30*u.fs,
        )
        sprofG = pp.Profile(
            profile    = "gaussian2D",
            fwhm       = 10*u.um,
        )
        lasGG=pp.Laser(
            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            time_profile    = tprofG,
            space_profile   = sprofG,
        )
        matAl  = pp.Material(
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u('amu'),
            Z           = 13 * u(''),
        )

        targAl = pp.Target(matAl)

        self.lpiGGAl = pp.LaserPlasmaInteraction(lasGG,targAl)
