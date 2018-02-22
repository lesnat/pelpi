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

# Print & save results
print("I0 = {}".format(laser.intensity()))
print("a0 = {}".format(laser.intensity_peak_normalized()))
nc = laser.electron.number_density_critical()

# Define a material
Al=pp.Material(
    density         = 2.69890e3 * u('kg/m**3'),
    atomic_mass     = 26.98154 * u('amu'),
    Z               = 13 * u(''),               # dimensionless unit
)

# Instanciate a Target object with a Material object
# TODO: add geometrical stuff via a Profile object
target=pp.Target(Al)

# Save & print results
ne = target.material.electron.number_density()
print("\nElectron density (in critical density)           : {}".format(ne/nc))



# Instanciate a LaserPlasmaInteraction object with Laser and Target objects
lpi=pp.LaserPlasmaInteraction(laser,target)

# Save & print some estimates
Teh = lpi.electron.hot.temperature(model="Haines2009")
print("\nHot electron temperature  (model = Haines2009)   : {}".format(Teh))

# TODO: *args in _Estimate
# n0 = lpi.electron.hot.number_total(model="Common",temperature=Teh,absorption_efficiency=0.4)
# print("Hot electron total number (model = Common)       : {}".format(n0))


# Compare to simulation/experiments
# ...

# Instanciate a ParticleInCell object with a LaserPlasmaInteraction object
pic=pp.ParticleInCell(lpi)

# Set default parameters
# lpi.electron.hot.set('temperature',Teh)

# Get estimates
dx=pic.length_cell('both',temperature=Teh)
Lr=pic.code.smilei.length()

print("\ndx           = {}        = {}".format(dx,dx/Lr))
resx=pic.space_resolution('both',temperature=Teh)
print("resx         = {}        = {}".format(resx,resx*Lr))
print("2 pi * resx  = {}".format(2 * np.pi * resx*Lr))
