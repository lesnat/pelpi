# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

import unittest

class test_Material(unittest.TestCase):
    def setUp(self):
        self.matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )

    def tearDown(self):
        del self.matAl

    def test_instanciate(self):
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )

    def test_electronNumberDensity(self):
        func = self.matAl.electronNumberDensity
        self.assertAlmostEqual(
            func().to('m**-3'),
            u.Quantity(7.830948876504127e+29, '1 / meter ** 3'))
        self.assertAlmostEqual(
            func(),
            self.matAl.ionNumberDensity() * self.matAl.Z,
            delta=u.Quantity(1e-7, 'kilogram / atomic_mass_unit / meter ** 3'))

    def test_ionNumberDensity(self):
        func = self.matAl.ionNumberDensity
        self.assertAlmostEqual(
            func().to('m**-3'),
            u.Quantity(6.023806828080096e+28, '1 / meter ** 3'))

# class test_Geometry(unittest.TestCase):
#     pass

class test_Target(unittest.TestCase):
    def setUp(self):
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )
        # geom = pp.Geometry(
        #     width=20 * u.um,
        #     Lpp=8 * u.um
        # )
        # self.targAl = pp.Target(matAl,geom)
        self.targAl = pp.Target(matAl)

    def tearDown(self):
        del self.targAl

    def test_instanciate(self):
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )
        # geom = pp.Geometry(
        #     width=20 * u.um,
        #     Lpp=8 * u.um
        # )
        # targAl = pp.Target(matAl,geom)
        targAl = pp.Target(matAl)
        # assert targAl.mat. ...


if __name__== '__main__':
    unittest.main()
