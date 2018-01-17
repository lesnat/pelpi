# coding:utf8
import sys
Modules_path="../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

laser=pp.Laser(
    name       = "eclipse4",

    wavelength = 0.8 * u.um,
    energy     = 2.0 * u.J,

    tprofile   = "gaussian",
    tfwhm      = 30 * u.fs,
    sprofile   = "gaussian",
    sfwhm      = 10 * u.um,

    contrast   = 1e8,

    polar      = [0,1,0],

    direction  = [0,0,1],
    angle      = 0. * u.deg,
)

mat=pp.Material(
    name        = "Al",
    density     = 2.69890e3 * u.kg/u.m**3,
    atomic_mass = 26.98154 * u.u,
    Z           = 13,
    A           = 27,
)
# mat=pp.Material(
#     name        = "W",
#     density     = 1.93000e4 * u.kg/u.m**3,
#     atomic_mass = 183.85 * u.u,
#     Z           = 74,
#     A           = 184,
# )

geom=pp.Geometry(
    width=20 * u.um,
    Lpp=8 * u.um
)

target=pp.Target(mat,geom)

lpi=pp.LaserPlasmaInteraction(laser,target)


print("sigma : " + str((lpi.getTargetConductivity()).to(u.ohm**-1 * u.m**-1)))
# print("sigma",(lpi.getTargetConductivity()).to(pp.prefered_unit['conductivity']))
print("nu : "+str((lpi.getLaserAbsorptionEfficiency())))
print("n0 : "+str((lpi.getHotElectronTotalNumber()).to_base_units()))

#
# pic=ParticleInCell(lpi)
# print(pic.getInfo())
