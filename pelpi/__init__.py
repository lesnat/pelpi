#coding:utf8
"""
Principle
=========
pelpi is an open source object-oriented python package designed to facilitate
physical estimations in the context of laser plasma interaction.

It can be helpfull for obtaining good estimates to design experimental setups,
or to constraint numerical parameters.
It can also be used to help interpreting results from different theoretical
backgrounds, or to validate simulation results with experimental scalings.

The general approach is to declare laser and target parameters only once,
and then to use theoretical models or experimental scalings to estimate
the desired physical quantities. Core objective of this approach is to obtain
in an easier way estimates that take several parameters, whose also needs
to be estimated from laser and target fundamental properties.

Some examples/tutorials can be found in examples/, and a most complete
documentation can be found in docs/reference.pdf or using help(pelpi) in python interpreter.

**Notes :**

- pelpi is actually specifically designed for ultra high intensity laser solid interaction, but also contains more general estimates and can be adapted to many other situations.
- pelpi is distributed under the GPL3 license. More details can be found in `LICENSE`.

Structure
=========
The pelpi package is based on object-oriented technology, as it is quite natural
to group target and laser properties in dedicated independant structures.
This approach also allows to build complex calculations in a simple way, by accessing
object properties instead of asking parameters to the user.

pelpi objects are :

- Profile, to define geometrical properties
- Laser, to define laser properties (such as pulse energy, temporal or spatial profile, ...)
- Material, to define material properties (such as atomic mass, density, ...)
- Target, to define target properties (such as material, geometry, ...)
- LaserPlasmaInteraction, to get estimates from models, with laser and target fundamental properties
- ParticleInCell, to get estimates of PIC numerical parameters

Units
=====
pelpi uses the python package ``pint`` to deal with unit conversion.

Its basic concept is to work with objects called ``Quantity``, containing a magnitude and a unit.
When operations are done under several ``Quantity`` objects, they are done on the magnitude and unit ;
so there is no need to care about conversion factor between different units.
Because of the structure of the pint package, operations between ``Quantity`` objects might
be done under the same unit registry. In pelpi it means that pint units might be **ONLY** accessed
via pelpi.unit object.
More informations can be found at http://pint.readthedocs.io/

Basic example
=============
Import the pelpi package

>>> import pelpi

Get a shortcut to the pint unit registry

>>> u = pelpi.unit

Instanciate a ``Target`` object

>>> Al = pelpi.Material(
...     density         = 2.69890e3 * u('kg/m**3'),
...     atomic_mass     = 26.98154 * u('amu'),
...     Z               = 13 * u(''),
... )
>>> target = pelpi.Target(Al)

Instanciate a ``Laser`` object

>>> laser=pelpi.Laser(
...     wavelength      = 0.8 * u.um,
...     energy          = 0.154 * u.J,
...
...     time_profile    = pelpi.Profile(profile = "gaussian1D", fwhm = 44 * u.fs),
...     space_profile   = pelpi.Profile(profile = "gaussian2D", fwhm = 12 * u.um)
... )

Instanciate a ``LaserPlasmaInteraction`` object with ``Laser`` and ``Target`` instances

>>> lpi=pelpi.LaserPlasmaInteraction(laser,target)

Loop over models to compare theoretical backgrounds

>>> for model in ['Beg1997','Haines2009','Wilks1992']:
...     Teh = lpi.electron.hot.temperature(model=model)
...     print("Hot electron temperature  (model = {})   : {:.4E}".format(model,Teh))

It is possible to get a shortcut to a specific sub-object as follows

>>> eh = lpi.electron.hot

Finally save one temperature value (model hypotheses are described in the doc)

>>> Teh = eh.temperature(model='Haines2009')

"""
# import _compat
__all__ = ["Profile","Material","Target","Laser","LaserPlasmaInteraction","ParticleInCell"]

__version__=0.3

import pint
unit=pint.UnitRegistry()

# TODO: default_unit & temperature via pint @context ?
default_unit={\
    'number'            : unit(''),\
    'length'            : unit('m'),\
    'time'              : unit('s'),\
    'mass'              : unit('kg'),\
    'energy'            : unit('J'),\
    'angle'             : unit('deg'),\
    'angular_frequency' : unit('s**-1'),\
    'density'           : unit('kg * m**-3'),\
    'number_density'    : unit('m**-3'),\
    'intensity'         : unit('W/m**2'),\
    'power'             : unit('W'),\
    'temperature'       : unit('MeV'),\
    'conductivity'      : unit('ohm**-1 * m**-1'),\
    'current'           : unit('A/m**2'),\
    'momentum'          : unit('kg * m / s'),\
    'electric_field'    : unit('kg * m / A / s**3'),\
    'magnetic_field'    : unit('kg / A / s'),\
}


from .profile import Profile
from .laser import Laser
from .target import Material,Target
from .lpi import LaserPlasmaInteraction
from .pic import ParticleInCell
