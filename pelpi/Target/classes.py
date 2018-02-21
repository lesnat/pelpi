#coding:utf8
from .._global import *
from .._tools import _PelpiObject


__all__ = ["Material","Target"]

class Material(_PelpiObject):
    """
    Class for defining material properties.
    
    Parameters
    ----------
    density : mass/length**3 Quantity
        Material density
    atomic_mass : mass Quantity
        Atomic or molecular mass
    Z : dimensionless Quantity
        Atomic number or number of charges per molecule
    """
    def __init__(self,density=None,atomic_mass=None,Z=None):
        # Test user input
        self._check_input('density'     ,density    ,type(_du['density']))
        self._check_input('atomic_mass' ,atomic_mass,type(_du['mass']))
        self._check_input('Z'           ,Z          ,type(_du['number']))
        
        # Initialize default dict
        self._initialize_defaults(input_dict={'density':density,'atomic_mass':atomic_mass,'Z':Z})

        # Instanciate sub-classes
        self.electron      = self._Electron(self)
        self.ion           = self._Ion(self)

    def density(self):
        """
        Returns
        -------
        User input `density` : mass/length**3 Quantity
        """
        return self.default['density']

    def atomic_mass(self):
        """
        Returns
        -------
        User input `atomic_mass` : mass Quantity
        """
        return self.default['atomic_mass']

    def Z(self):
        """
        Return user input `Z`.
        """
        return self.default['Z']

    class _Electron(_PelpiObject):
        """
        Electron properties.
        """
        def __init__(self,material):
            # No need to check input because this method is only called in Material definition.
            
            # Initialize default dict
            self._initialize_defaults()
            
            # Save reference to Material instance in a private variable
            self._mat = material

        def number_density(self):
            """
            Returns
            -------
            Electron number density : 1/length**3 Quantity
            """
            if self.default['number_density'] is not None:
                return self.default['number_density']
            else:
                Z           = self._mat.Z()
                rho         = self._mat.density()
                am          = self._mat.atomic_mass()

                ne          = (Z*rho/am)
                return ne.to(_du['number_density'])

    class _Ion(_PelpiObject):
        """
        Ion properties.
        """
        def __init__(self,material):
            # No need to check input because this method is only called in Material definition.

            # Initialize default dict
            self._initialize_defaults()
            
            # Save reference to Material instance in a private variable
            self._mat = material

        def number_density(self):
            """
            Returns
            -------
            Ion number density : 1/length**3 Quantity
            """
            if self.default['number_density'] is not None:
                return self.default['number_density']
            else:
                rho         = self._mat.density()
                am          = self._mat.atomic_mass()
                
                ni          = rho/am
                return ni.to(_du['number_density'])

class Target(_PelpiObject):
    """
    Class for defining the target characteristics.
    
    Parameters
    ----------
    material : object
        Instanciated ``Material`` pelpi object
        
    Attributes
    ----------
    material : object
        Input material object
    """
    def __init__(self,material):
        # Test user input
        self._check_input('material',material,"<class 'pelpi.Target.classes.Material'>")
        
        # Initialize default dict
        self._initialize_defaults()
        
        # Save reference to Material instance
        self.material=material
