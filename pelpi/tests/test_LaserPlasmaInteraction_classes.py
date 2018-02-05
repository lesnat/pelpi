# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

from examples import ExampleLPI

import pelpi as pp
u=pp.unit

import unittest


class test_LaserPlasmaInteraction(unittest.TestCase):
    def setUp(self):
        self.lpiGGAl = ExampleLPI().lpiGGAl

    def tearDown(self):
        del self.lpiGGAl

class test_Electron(unittest.TestCase):
    def setUp(self):
        self.lpiGGAl = ExampleLPI().lpiGGAl

    def tearDown(self):
        del self.lpiGGAl

class test_Electron_Cold(unittest.TestCase):
    def setUp(self):
        self.lpiGGAl = ExampleLPI().lpiGGAl

    def tearDown(self):
        del self.lpiGGAl


class test_Electron_Hot(unittest.TestCase):
    def setUp(self):
        self.lpiGGAl = ExampleLPI().lpiGGAl

    def tearDown(self):
        del self.lpiGGAl

    def test_numberTotal(self):
        pass
        # func=self.lpiGGAl.electron.hot.numberTotal
        # # Bell1997 model with lpiGGAl interaction
        # Teh = self.lpiGGAl.electron.hot.temperature(model="Haines2009")
        # Zeff = self.lpiGGAl.ion.ionisationRange(model=,temperature=Te)
        # log_coulomb = self.lpiGGAl.target.logCoulomb(model=,ionisation_range=Zeff)
        # Tec = self.lpiGGAl.electron.cold.temperature(model=)
        # Sigma = self.lpiGGAl.target.conductivity(model="Hubbard1966",temperature=Tec,log_coulomb=log_coulomb)
        # nu_laser = self.lpiGGAl.laser.absorptionEfficiency(model=)
        # self.assertAlmostEqual(
        #     func(model="Bell1997",temperature=Te,conductivity=Sigma,absorption_efficiency=nu_laser),
        #     0)

        # # TODO: argument loop=True -> loop over all the models with a checkHypotheses and try, except for getting the max value for ex. (func=max in arguments and return func(list))
        # # TODO: generic procedure : testing if in available_models and generic checkHypotheses + return model(**kwargs) ?
        # if model=="Bell1997":
        #     Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
        #     Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
        #     nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
        #     Model   = _m.Model.Bell1997(self)
        #     Model.checkHypotheses()
        #     nehTot = Model.numberTotal(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet
        # elif model=="Obvious":
        #     Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
        #     Model=_m.Model.Obvious(self)
        #     nehTot = Model.numberTotal(Teh)
        # else:
        #     raise NameError("Unknown model name.")
        #
        # return nehTot

    def test_lengthCaracDepth(self):
        pass

    def test_temperature(self):
        #lpiGGAl case
        func = self.lpiGGAl.electron.hot.temperature
        # Beg1997 model
        self.assertAlmostEqual(
            func(model="Beg1997").to('MeV'),
            u.Quantity(0.7072354609042557, 'megaelectron_volt'))
        # Haines2009 model
        self.assertAlmostEqual(
            func(model="Haines2009").to('MeV'),
            u.Quantity(0.9477748467520224, 'megaelectron_volt'))
        # Wilks1992 model
        self.assertAlmostEqual(
            func(model="Wilks1992").to('MeV'),
            u.Quantity(2.122419582112406, 'megaelectron_volt'))

        with self.assertRaises(TypeError):
            func(model=47)

        with self.assertRaises(NameError):
            func(model='47')

        # for model_name in ['47',47]:
        #     self.assertRaises(
        #         NameError,
        #         func,
        #         model_name)



    def test_timeInteractionMax(self,verbose=True):
        pass

    def test_lengthInteractionMax(self,verbose=True):
        pass


if __name__== '__main__':
    unittest.main()
