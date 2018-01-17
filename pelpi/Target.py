#coding:utf8
import numpy as _np
from . import unit
from . import prefered_unit as _pu


__all__ = ["Material","Geometry","Target"]

class Material(object):
    """
    """
    def __init__(self,name="",density=None,atomic_mass=None,Z=None,A=None): # TODO: which initialisation ?
        if name=="": # TODO: read in database
            print("Define")
        elif name=="Al":
            self.name       = name
            self.density    = 2.69890e3 * unit.kg/unit.m**3
            self.atomic_mass = 26.98154 * unit.u
            self.Z          = 13
            self.A          = 27
        elif name=="W":
            self.name       = name
            self.density    = 1.93000e4 * unit.kg/unit.m**3
            self.atomic_mass = 183.85 * unit.u
            self.Z          = 74
            self.A          = 184
        # elif name=="CH":
        #     self.name       = name
        #     self.density    =
        #     self.atomic_mass= 13.018 * unit.g/unit.mol
        #     self.Z          = 0
        #     self.A          = 0
        else:
            self.name       = name
            self.density    = density * unit.kg/unit.m**3
            self.atomic_mass = atomic_mass * unit.u
            self.Z          = Z
            self.A          = A

        def name(self):
            return self.name

        def density(self):
            return self.density

        def Z(self):
            return self.Z

        def A(self):
            return self.A

        def N(self):
            return self.Z-self.A

        def electronDensity(self): # TODO: class electron method density ?
            return self.Z*self.density/self.atomic_mass

        def ionDensity(self):
            return self.density/self.atomic_mass

class Geometry(object): # Ajouter pp
    """
    """
    def __init__(self,width=0,Lpp=0):
        self.width      = width
        self.Lpp        = Lpp

class Target(object):
    """



    """
    def __init__(self,Material,Geometry):
        self.mat=Material
        self.geom=Geometry
