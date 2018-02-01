#coding:utf8
"""

Module documentation ...

"""
__all__ = ["Profile","Material","Geometry","Target","Laser","LaserPlasmaInteraction"]

import pint
unit=pint.UnitRegistry()

# TODO: voire prefered unit et temperature via @context
prefered_unit={'intensity':unit.W/unit.cm**2,'energy':unit.J,'length':unit.um,'time':unit.fs,\
    'angle':unit.deg,'pulsation':unit.s**-1,'density':unit.kg * unit.m**-3,\
    'number density':unit.m**-3,'power':unit.TW,'temperature':unit.MeV,\
    'mass':unit.kg,'conductivity':unit.ohm**-1 * unit.m**-1, \
    'number':unit(''),'electric field':unit(''),'magnetic field':unit('')}# TODO: change E/B field


import warnings
warnings.formatwarning = lambda message, category, filename, lineno, line : \
    "\n"+'%s:%s:%s\n    %s : %s' % (filename,lineno,line, category.__name__,message)+"\n"
warnings.simplefilter('always',UserWarning)


from .Laser.classes import Laser,Profile
from .Target.classes import Material,Target
from .LaserPlasmaInteraction.classes import LaserPlasmaInteraction
from .ParticleInCell.classes import ParticleInCell
