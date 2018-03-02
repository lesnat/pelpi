# coding:utf8
"""
03-get_complex_estimates
========================

This example shows how to use simple ``LaserPlasmaInteraction`` estimates
for building a more complex one.


Explanations
------------
TODO


"""
# Add pelpi path to python path
import sys
pelpi_path="../"
if sys.path[0]!=pelpi_path:sys.path.insert(0, pelpi_path)

# Import packages
import pelpi as pp

# Get a shortcut to the pint unit registry
u = pp.unit

# Instanciate a ``Target`` object
Al = pp.Material(
    density         = 2.69890e3 * u('kg/m**3'),
    atomic_mass     = 26.98154 * u('amu'),
    Z               = 13 * u(''),
)

target = pp.Target(Al)

# Instanciate a ``Laser`` object
laser=pp.Laser(
    wavelength      = 0.8 * u.um,
    energy          = 0.154 * u.J,

    time_profile    = pp.Profile(profile = "gaussian1D", fwhm = 44 * u.fs),
    space_profile   = pp.Profile(profile = "gaussian2D", fwhm = 12 * u.um)
)

# Instanciate a ``LaserPlasmaInteraction`` object with ``Laser`` and ``Target`` instances
lpi=pp.LaserPlasmaInteraction(laser,target)

# Save one temperature estimate
eh = lpi.electron.hot
Teh = eh.temperature(model='Haines2009')


