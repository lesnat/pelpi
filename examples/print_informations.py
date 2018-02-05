# coding:utf8
import sys
Modules_path="../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

# Import modules
import numpy as np
import pelpi as pp
u=pp.unit

# Set user units (default : SI).
# More informations about units can be found in the pint package documentation
pp.default_unit['energy']      = u('MeV')      # Units can be defined like this
pp.default_unit['temperature'] = u('MeV')
pp.default_unit['length']      = u.um          # or like this
pp.default_unit['time']        = u('fs')
pp.default_unit['intensity']   = u.W/u.cm**2   # and can be combined
pp.default_unit['power']       = u('TW')       # It accepts prefixes # long names or short

# Define temporal and spatial laser profiles
tprof=pp.Profile(
    profile         = "gaussian1D",             # Check the doc for available profiles
    fwhm            = 44 * u.fs,                # Always define value + unit
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

# Print informations
print("I0 = {}".format(laser.intensity()))
print("a0 = {}".format(laser.intensity_peak_normalized()))

# Define a material
Al=pp.Material(
    density         = 2.69890e3 * u('kg/m**3'),
    atomic_mass     = 26.98154 * u('amu'),
    Z               = 13 * u(''),               # dimensionless unit
)

# Instanciate a Target object with a Material object
# TODO: add geometrical stuff via a Profile object
target=pp.Target(Al)

# Save important values to a variable
ne = target.material.electron.number_density()


# Instanciate a LaserPlasmaInteraction object with Laser and Target objects
lpi=pp.LaserPlasmaInteraction(laser,target)

# Print some estimates
# print("sigma : " + str((lpi.getTargetConductivity()).to(u.ohm**-1 * u.m**-1)))
# # print("sigma",(lpi.getTargetConductivity()).to(pp.default_unit['conductivity']))
# print("nu : "+str((lpi.getLaserAbsorptionEfficiency())))
# print("n0 : "+str((lpi.getHotElectronTotalNumber()).to_base_units()))


# Set defaults
Teh = lpi.electron.hot.temperature(model="Haines2009")
# lpi.electron.hot.set('temperature',Teh)

# Plot some results
# ... # Here the default temperature is used

# Instanciate a ParticleInCell object with a LaserPlasmaInteraction object
pic=pp.ParticleInCell(lpi)

# Get some estimates
dx=pic.length_cell(temperature=Teh)
print("dx           = {}        = {}".format(dx,dx/pic.code.length()))
resx=pic.space_resolution(temperature=Teh)
print("resx         = {}        = {}".format(resx,resx*pic.code.length()))
print("2 pi * resx  = {}".format(2 * np.pi * resx*pic.code.length()))
