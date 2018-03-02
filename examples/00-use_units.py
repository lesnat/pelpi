# coding:utf8
"""
00-use_units
============

This example shows how to use pint units.


Explanations
------------
pint is a python package created to manipulate physical quantities easily.

Its basic concept is to work with objects called ``Quantity``, containing a magnitude and a unit.
When operations are done under several ``Quantity`` objects, they are done on the magnitude and unit ;
so there is no need to care about conversion factor between different units.
Because of the structure of the pint package, operations between ``Quantity`` objects might
be done under the same unit registry. In pelpi it means that pint units might be **ONLY** accessed
via pelpi.unit object.
More informations can be found at http://pint.readthedocs.io/
"""
# Add pelpi path to python path
import sys
pelpi_path="../"
if sys.path[0]!=pelpi_path:sys.path.insert(0, pelpi_path)

# Import packages
import numpy as np
import pelpi

# Get a shortcut to the pint unit registry
u = pelpi.unit

# Declare pint ``Quantity`` objects
### Units can be found explicitly via str
laser_wavelength    = 0.8e-6  * u('meter')
### or with short names as attributes
laser_energy        = 1.0     * u.J
### It accepts prefixes (here tera watt)
laser_peak_power    = 21.0    * u.TW
### and can be combined
laser_peak_intensity= 1.4e19  * u('W/cm**2')

# Calculate something from it
I0 = laser_peak_intensity
ll = laser_wavelength
laser_normalized_peak_intensity = 0.85 * np.sqrt((I0 * ll**2)/(1e18 * u('W/cm**2 * um**2')))

# Convert units
### Print laser wavelength converted to micrometer with 4 digits precision
print("laser wavelength : {:.4E}".format(ll.to('um')))
### Change laser peak intensity unit to W/m**2
laser_peak_intensity.ito('W/m**2')
### Change laser normalized peak intensity unit to base units (SI units)
laser_normalized_peak_intensity.ito_base_units()
