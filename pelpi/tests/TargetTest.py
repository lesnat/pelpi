# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

class MaterialTest(object):
    def instanciateTest(self):
        self.matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )


    def nameTest(self):
        pass
        # assert self.matAl.name ==

    def densityTest(self):
        pass
        # assert self.matAl.density ==

    def atomic_massTest(self):
        pass
        # assert self.matAl.atomic_mass ==

    def ZTest(self):
        pass
        # assert self.matAl.Z ==

    def ATest(self):
        pass
        # assert self.matAl.A ==

    def NTest(self):
        pass
        # assert self.matAl.N ==

    def electronDensityTest(self):
        pass
        # assert self.matAl.electronDensity ==

    def ionDensityTest(self):
        pass
        # assert self.matAl.ionDensity ==

class GeometryTest(object):
    pass

class TargetTest(object):
    def instanciateTest(self):
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )
        geom = pp.Geometry(
            width=20 * u.um,
            Lpp=8 * u.um
        )
        self.targAl = pp.Target(matAl,geom)
