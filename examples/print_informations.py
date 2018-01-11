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

print(laser.getInfo())
laser.plot()

mat=pp.Material(
    name="Al"
)

geom=pp.Geometry(
    width=20 * u.um,
    Lpp=8 * u.um
)

target=pp.Target(mat,geom)
print(target.getInfo())


lpi=pp.LaserPlasmaInteraction(laser,target)
print(lpi.getInfo())


print("sigma : " + str((lpi.getTargetConductivity()).to(u.ohm**-1 * u.m**-1)))
# print("sigma",(lpi.getTargetConductivity()).to(pp.prefered_unit['conductivity']))
print("nu : "+str((lpi.getLaserAbsorptionEfficiency())))
print("n0 : "+str((lpi.getHotElectronTotalNumber()).to_base_units()))

#
# pic=ParticleInCell(lpi)
# print(pic.getInfo())
