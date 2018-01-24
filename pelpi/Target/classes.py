#coding:utf8
from .._global import *
from .._tools import _PelpiObject


__all__ = ["Material","Target"]

class Material(object):
    """
    Class for defining a material.

    """
    def __init__(self,density,atomic_mass,Z,A): # TODO: which initialisation ?
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
    Class for defining the target characteristics.
    """
    def __init__(self,Material):
        self.material=Material
