#coding:utf8
"""

Module documentation ...

"""
# import _compat
__all__ = ["Profile","Material","Target","Laser","LaserPlasmaInteraction","ParticleInCell"]

import pint
unit=pint.UnitRegistry()

# TODO: default_unit & temperature via pint @context ?
default_unit={\
    'number'        : unit(''),\
    'length'        : unit('m'),\
    'time'          : unit('s'),\
    'mass'          : unit('kg'),\
    'energy'        : unit('J'),\
    'angle'         : unit('deg'),\
    'pulsation'     : unit('s**-1'),\
    'density'       : unit('kg * m**-3'),\
    'number_density': unit('m**-3'),\
    'intensity'     : unit('W/m**2'),\
    'power'         : unit('W'),\
    'temperature'   : unit('MeV'),\
    'conductivity'  : unit('ohm**-1 * m**-1'),\
    'current'       : unit('A/m**2'),\
    'momentum'      : unit('kg * m / s'),\
    'electric_field': unit('kg * m / A / s**3'),\
    'magnetic_field': unit('kg / A / s'),\
}


from .Profile import Profile
from .Laser import Laser
from .Target import Material,Target
from .LaserPlasmaInteraction import LaserPlasmaInteraction
from .ParticleInCell import ParticleInCell
