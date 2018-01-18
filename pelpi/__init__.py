#coding:utf8
"""
Module documentation ...

"""
__all__ = ["Material","Geometry","Target","Laser","LaserPlasmaInteraction","Model"]

# import _global

import pint

# TODO: Voire pour définition variables globales, fichier _global.py ?
# global unit
unit=pint.UnitRegistry()

# TODO: voire prefered unit et temperature via @context
# global prefered_unit
prefered_unit={'intensity':unit.W/unit.cm**2,'energy':unit.J,'length':unit.um,'time':unit.fs,\
    'angle':unit.deg,'pulsation':unit.s**-1,'density':unit.kg * unit.m**-3,'number density':unit.m**-3,'power':unit.TW,'temperature':unit.MeV,\
    'mass':unit.kg,'conductivity':unit.ohm**-1 * unit.m**-1}

# TODO: voire pour verbosities dans checkHypotheses
# global verbosities
verbose=True

from .Laser import Laser,Profile
from .Target import Material,Geometry,Target
from .LaserPlasmaInteraction import LaserPlasmaInteraction
from .ParticleInCell import ParticleInCell
