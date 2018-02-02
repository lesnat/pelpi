# coding:utf8
import sys
Modules_path="../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import numpy as np

import pelpi as pp
u=pp.unit

tprof=pp.Profile(
    profile    = "gaussian1D",
    fwhm       = 44 * u.fs,
)
sprof=pp.Profile(
    profile    = "gaussian2D",
    fwhm       = 12 * u.um
)

laser=pp.Laser(
    wavelength = 0.8 * u.um,
    energy     = 0.154 * u.J,

    time_profile = tprof,
    space_profile = sprof
)

print("I0 = {}".format(laser.intensity().to(pp.prefered_unit['intensity'])))
print("a0 = {}".format(laser.intensity_peak_normalized().to('')))

mat=pp.Material(
    density     = 2.69890e3 * u('kg/m**3'),
    atomic_mass = 26.98154 * u('amu'),
    Z           = 13 * u(''),
)
# mat=pp.Material(
#     density     = 1.93000e4 * u('kg/m**3'),
#     atomic_mass = 183.85 * u('u'),
#     Z           = 74 * u(''),
#     A           = 184 * u(''),
# )

target=pp.Target(mat)

lpi=pp.LaserPlasmaInteraction(laser,target)


# print("sigma : " + str((lpi.getTargetConductivity()).to(u.ohm**-1 * u.m**-1)))
# # print("sigma",(lpi.getTargetConductivity()).to(pp.prefered_unit['conductivity']))
# print("nu : "+str((lpi.getLaserAbsorptionEfficiency())))
# print("n0 : "+str((lpi.getHotElectronTotalNumber()).to_base_units()))


pic=pp.ParticleInCell(lpi)

Teh = lpi.electron.hot.temperature(model="Haines2009")

dx=pic.length_cell(temperature=Teh)
print("dx           = {}        = {}".format(dx,dx/pic.code.length()))
resx=pic.space_resolution(temperature=Teh)
print("resx         = {}        = {}".format(resx,resx*pic.code.length()))
print("2 pi * resx  = {}".format(2 * np.pi * resx*pic.code.length()))
