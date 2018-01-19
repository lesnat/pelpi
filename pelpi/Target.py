#coding:utf8
import numpy as _np
from . import unit as _u
from . import prefered_unit as _pu


__all__ = ["Material","Target"]

class Material(object):
    """
    """
    def __init__(self,name,density,atomic_mass,Z,A): # TODO: which initialisation ?
        self.name       = name
        self.density    = density
        self.atomic_mass = atomic_mass
        self.Z          = Z
        self.A          = A
        self.N          = A-Z

    def electronNumberDensity(self): # TODO: class electron method density ?
        return self.Z*self.density/self.atomic_mass

    def ionNumberDensity(self):
        return self.density/self.atomic_mass

class Target(object):
    """
    """
    def __init__(self,Material):
        self.material=Material
