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
        self.electron      = self._Electron(self)
        self.ion           = self._Ion(self)

    def density(self):
        return self._density

    def atomic_mass(self):
        return self._atomic_mass

    def Z(self):
        return self._Z

    class _Electron(_PelpiObject):
        def __init__(self,Material):
            self._mat = Material

        def number_density(self): # TODO: class electron method density ?
            """
            Return electron number density.
            """

            Z           = self._mat.Z()
            rho         = self._mat.density()
            am          = self._mat.atomic_mass()

            ne          = (Z*rho/am) # TODO: Return default value if define, or result
            return ne.to(_du['number_density'])

    class _Ion(_PelpiObject):
        def __init__(self,Material):
            self._mat = Material

        def number_density(self):
            rho         = self._mat.density()
            am          = self._mat.atomic_mass()
            return (rho/am).to(_du['number_density'])

class Target(_PelpiObject):
    """
    Class for defining the target characteristics.
    """
    def __init__(self,Material):
        self.material=Material
