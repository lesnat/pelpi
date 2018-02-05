#coding:utf8
"""

Module documentation ...

"""
__all__ = ["Profile","Material","Geometry","Target","Laser","LaserPlasmaInteraction"]

import pint
unit=pint.UnitRegistry()

# TODO: voire prefered unit et temperature via @context
default_unit={\
    'number':unit(''),\
    'length':unit('m'),\
    'time':unit('s'),\
    'mass':unit('kg'),\
    'energy':unit('J'),\
    'angle':unit('deg'),\
    'pulsation':unit('s**-1'),\
    'density':unit('kg * m**-3'),\
    'number_density':unit('m**-3'),\
    'intensity':unit('W/m**2'),\
    'power':unit('TW'),\
    'temperature':unit('MeV'),\
    'conductivity':unit('ohm**-1 * m**-1'),\
    'current':unit('A/m**2'),\
    'momentum':unit('kg * m / s'),\
    'electric_field':unit('kg * m / A / s**3'),\
    'magnetic_field':unit('kg / A / s'),\
}

from .Profile.classes import Profile
from .Laser.classes import Laser
from .Target.classes import Material,Target
from .LaserPlasmaInteraction.classes import LaserPlasmaInteraction
from .ParticleInCell.classes import ParticleInCell
