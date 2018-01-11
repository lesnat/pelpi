#coding:utf8
"""
Module documentation ...

"""
import pint

unit=pint.UnitRegistry()


prefered_unit={'intensity':unit.W/unit.cm**2,'energy':unit.J,'length':unit.um,'time':unit.fs,\
    'angle':unit.deg,'pulsation':unit.s**-1,'density':unit.m**-3,'power':unit.TW,'temperature':unit.MeV,\
    'mass':unit.kg,'conductivity':unit.ohm**-1 * unit.m**-1}


from .Laser import *
from .Target import *
from .LaserPlasmaInteraction import *

from .Model import * 

# from ParticleInCell import *
