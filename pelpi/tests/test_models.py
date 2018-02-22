# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

from examples import ExampleLPI,PelpiTest

import pelpi as pp
u=pp.unit

import unittest

################################################################################
class ExampleModelTest(PelpiTest):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_example_method(self):
        pass
        

################################################################################
class test_Beg1997(PelpiTest):
    def setUp(self):
        self.lpiGGAl=ExampleLPI().lpiGGAl
        
    def tearDown(self):
        del self.lpiGGAl
        
    def test_electron_hot_temperature(self):
        self.assertAlmostEqualQuantity(\
        self.lpiGGAl.electron.hot.temperature(model="Beg1997"),\
        7.072354609042559E-01 * u('MeV'))
        
    def test_ion_energy_cutoff(self):
        pass

class test_Haines2009(PelpiTest):
    def setUp(self):
        self.lpiGGAl=ExampleLPI().lpiGGAl
        
    def tearDown(self):
        del self.lpiGGAl
    
    def electron_hot_temperature(self):
        self.assertAlmostEqualQuantity(\
        self.lpiGGAl.electron.hot.temperature(model="Haines2009"),\
        9.477748467520224E-01 * u('MeV'))


class test_Price1995(PelpiTest):
    def setUp(self):
        self.lpiGGAl=ExampleLPI().lpiGGAl
        
    def tearDown(self):
        del self.lpiGGAl
    
    def electron_hot_temperature(self):
        self.assertAlmostEqualQuantity(\
        self.lpiGGAl.electron.absorption_efficiency(model="Price1995"),\
        0.1 * u(''))


class test_Wilks1992(PelpiTest):
    def setUp(self):
        self.lpiGGAl=ExampleLPI().lpiGGAl
        
    def tearDown(self):
        del self.lpiGGAl
    
    def electron_hot_temperature(self):
        self.assertAlmostEqualQuantity(\
        self.lpiGGAl.electron.hot.temperature(model="Wilks1992"),\
        2.122419582112406E+00 * u('MeV'))
                

################################################################################

class test_Common(PelpiTest):
    def setUp(self):
        self.lpiGGAl=ExampleLPI().lpiGGAl
        
    def tearDown(self):
        del self.lpiGGAl
    
    def electron_number_total(self):
        Te = 1 * u('MeV')
        eta_l = 0.1 * u('')
        self.assertAlmostEqualQuantity(\
        self.lpiGGAl.electron.number_total(model="Common",temperature = Te, absorption_efficiency = eta_l),\
        8.322012639476957E+11 * u(''))
    
    def test_electron_distribution(self):
        pass
        
        
        
        
        
################################################################################
if __name__== '__main__':
    unittest.main()
