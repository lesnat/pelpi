#coding:utf8
from .._global import *
from .._tools import _PelpiObject
from ..Target.database import _MaterialDatabase


__all__ = ["Material","Target"]

class Material(_PelpiObject):
    """
    Class for defining a material.

    """
    database = _MaterialDatabase()

    def __init__(self,density,atomic_mass,Z,A): # TODO: which initialisation ?
        var_dict={\
            'density':density,\
            'atomic_mass':atomic_mass,\
            'Z':Z,\
            'A':A\
        }
        super(Material,self).__init__(var_dict)

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
