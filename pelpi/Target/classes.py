#coding:utf8
from .._global import *
from .._tools import _PelpiObject,_Electron
# from ..Target.database import _MaterialDatabase


__all__ = ["Material","Target"]

class Material(_PelpiObject):
    """
    Class for defining a material.

    """
    # database = _MaterialDatabase()

    def __init__(self,density,atomic_mass,Z): # TODO: which initialisation ?
        self._density      = density
        self._atomic_mass  = atomic_mass
        self._Z            = Z

    def density(self):
        return self._density

    def atomic_mass(self):
        return self._atomic_mass

    def Z(self):
        return self._Z

    def electronNumberDensity(self): # TODO: class electron method density ?
        """
        Return electron number density.
        """

        Z           = self.Z()
        rho         = self.density()
        am          = self.atomic_mass()

        ne          = self._dor(Z*rho/am) # Return default value if define, or result
        return ne.to(_pu['number density'])

    def ionNumberDensity(self):
        rho         = self.density()
        am          = self.atomic_mass()
        return (rho/am).to(_pu['number density'])

class Target(_PelpiObject):
    """
    Class for defining the target characteristics.
    """
    def __init__(self,Material):
        self.material=Material
