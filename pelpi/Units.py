# coding:utf8
import numpy as np

pi         = np.pi

c          = 299792458             # m.s^-1
mu0        = 4*pi*1e-7

e          = 1.6021766208e-19              # C (A.s)
G          = 6.67408e-11
h          = 6.626070040e-34
kb         = 1.38064852e-23
me         = 9.10938356e-31              # kg
mp         = 1.672621898e-27

hbar       = h/(2*pi)
epsilon0   = 1/(mu0*c**2) # F.m-1 (A^2.s^4.kg^-1.m^-3)
alpha      = e**2/(4*pi*epsilon0*hbar*c)


eV         = e
uma        = 1.660538921e-27       # kg


SI={'mass':'kg','time':'s','length':'m','energy':'J'}
cgs={'mass':'g','time':'s','length':'cm','energy':'erg'}
PIC={'density':'nc','time':'Tr','length':'Lr','energy':'me c2'}
User={'intensity':'W/cm2','energy':'MeV','length':'um','time':'fs'}

def sciFormat(var):
    return "%.2E" % var

def decFormat(var):
    return "%.2F" % var



def convToSI(var,unit):
    pass

def convFromSI(var,unit):
    pass

def convNoSI(var,unit1,unit2):
    return convfromSI(conv2SI(var,unit1),unit2)
