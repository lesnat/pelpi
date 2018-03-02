# coding:utf8
"""
01-instanciate_objects
======================

This example shows how to instanciate pelpi objects,
and how to get basic calculation results from instance methods.


Explanations
------------
The pelpi package is based on object-oriented technology, as it is quite natural
to group target and laser properties in dedicated independant structures.
This approach also allows to build complex calculations in a simple way, by accessing
object properties instead of asking parameters to the user.

Base pelpi objects are :
- Profile, to define geometrical properties
- Laser, to define laser properties (such as pulse energy, temporal or spatial profile, ...)
- Material, to define material properties (such as atomic mass, density, ...)
- Target, to define target properties (such as material, geometry, ...)
- LaserPlasmaInteraction, to get estimates from models, with laser and target fundamental properties
- ParticleInCell, to get estimates of PIC numerical parameters

Input parameters of those objects are then pint ``Quantity``, strings or pelpi object instances.
Once the object is instanciated, those parameters can be accessed from methods (for string or Quantity)
or attributes (for pelpi instances).

It was choosen to let the user only access methods and sub-objects as attributes,
that way input values can not be overriden accidentaly and the interface is more coherent.

See the doc for more information about a specific object.
"""
# Add pelpi path to python path
import sys
pelpi_path="../"
if sys.path[0]!=pelpi_path:sys.path.insert(0, pelpi_path)

# Import packages
import pelpi as pp

# Get a shortcut to the pint unit registry
u = pp.unit

# Instanciate a ``Material`` object
### Documentation about input parameters
### can be found in docs/reference.pdf or using help(pelpi.Material)
Al = pp.Material(
    density         = 2.69890e3 * u('kg/m**3'), # Always define value + unit
    atomic_mass     = 26.98154  * u('amu'),     # atomic mass unit
    Z               = 13        * u(''),        # dimensionless unit
)

# Instanciate a ``Target`` object from the ``Material`` instance
target = pp.Target(Al)

# Get access to input parameters
### Material input parameter can be accessed
### from a method of the 'material' attribute of Target instance
rho   = target.material.density()
M_at  = target.material.atomic_mass()           # Accessible only from methods

# Get calculation results
### Number of ions per unit volume
ni = target.material.ion.number_density()       # rho/M_at
### Number of electrons per unit volume
ne = target.material.electron.number_density()  # Z * ni

# Define temporal and spatial laser profiles
tprof=pp.Profile(
    profile         = "gaussian1D",             # See the doc for available profiles
    fwhm            = 44 * u.fs,
)
sprof=pp.Profile(
    profile         = "gaussian2D",
    fwhm            = 12 * u.um
)

# Define laser from profiles
laser=pp.Laser(
    wavelength      = 0.8 * u.um,
    energy          = 0.154 * u.J,

    time_profile    = tprof,
    space_profile   = sprof
)

# Get other results
I0 = laser.intensity(r=0*u.um,t=0*u.fs)
a0 = laser.intensity_peak_normalized()
nc = laser.electron.number_density_critical()

# and combine them
print("Target ion number density (in nc)      : {:.2F}".format(ni/nc))
print("Target electron number density (in nc) : {:.2F}".format(ne/nc))

