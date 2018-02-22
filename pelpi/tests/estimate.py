#coding:utf8
"""
Script doing some estimates, to help writing tests about Quantity objects (mostly in test_models).
"""

import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)
import pelpi as pp
u=pp.unit

from examples import ExampleLPI

lpiGGAl=ExampleLPI().lpiGGAl

SEPARATOR="\n ################################################ \n"

print(SEPARATOR)
print(' Estimates for Profile test class')
print(SEPARATOR)

print(' lpiGGAl : integral1D = {:.15E}'.format(lpiGGAl.laser.time_profile.integral1D()))
print(' lpiGGAl : integral2D = {:.15E}'.format(lpiGGAl.laser.space_profile.integral2D()))

print(SEPARATOR)
print(' Estimates for Laser test class')
print(SEPARATOR)



print(SEPARATOR)
print(' Estimates for Material test class')
print(SEPARATOR)



print(SEPARATOR)
print(' Estimates for Target test class')
print(SEPARATOR)




print(SEPARATOR)
print(' Estimates for LaserPlasmaInteraction test class')
print(SEPARATOR)




print(SEPARATOR)
print(' Estimates for models test class')
print(SEPARATOR)

print(' lpiGGAl : hot electron temperature')
for model in ['Beg1997','Haines2009','Wilks1992']:
    Teh = lpiGGAl.electron.hot.temperature(model=model)
    print("     model : {}     Teh = {:.15E}".format(model,Teh))


print(' lpiGGAl : electron total number')
for model in ['Common']:
    Te = 1 * u('MeV')
    eta_l = 0.1 * u('')
    
    neh = lpiGGAl.electron.number_total(model="Common",temperature = Te, absorption_efficiency = eta_l)
    print("     model : {}     neh = {:.15E}".format(model,neh))

    

