#coding:utf8

from ._global import *
from ._tools import _PelpiObject,_Default,_estimate

class _PlasmaParameters(_PelpiObject):
    """
    Class containing usual plasma parameters.
    """
    def __init__(self,LaserPlasmaInteraction):
        # No need to check input because this method is only called in LaserPlasmaInteraction definition

        # Do not initialize default dict because there is no direct access to a method from this point ???

        # Save reference to LaserPlasmaInteraction instance in a private variable
        self._lpi   = LaserPlasmaInteraction

        # Instanciate sub-classes
        self.electron         = _PlasmaElectron(self._lpi)
        self.ion              = _PlasmaIon(self._lpi)


class _PlasmaElectron(_PelpiObject):
    """
    Plasma parameters about electrons.
    """
    def __init__(self,LaserPlasmaInteraction):
        # No need to check input because this method is only called in _PlasmaParameters definition

        # Initialise default dict
        self.default = _Default(self)

        # Save reference to LaserPlasmaInteraction instance in a private variable
        self._lpi   = LaserPlasmaInteraction

    def length_Debye(self,temperature):
        """
        Returns
        -------
        Debye length of electrons : length Quantity

        Notes
        -----
        The Debye length is defined as

        .. math:: \lambda_{De} = \sqrt{\\frac{\epsilon_0 T_e}{n_e e^2}}
        """
        dim = 'length'
        ne  = self._lpi.target.material.electron.number_density()
        Te  = temperature
        LDe = _np.sqrt((_u.epsilon_0 * Te)/(ne * _u.e**2))
        
        return self.default.result('length_Debye',LDe,dim)


    def length_Landau(self,temperature):
        """
        Returns
        -------
        Landau length of electrons : length Quantity

        Notes
        -----
        The Landau length is defined as

        .. math:: r_0 = \\frac{e^2}{4 \pi \epsilon_0 T_e}
        """
        dim = 'length'
        Te  = temperature
        LLa = ((_u.e**2)/(4*_np.pi * _u.epsilon_0 * Te)) # TODO: OK ? check
        
        return self.default.result('length_Landau',LLa,dim)

    def angular_frequency_plasma(self):
        """
        Returns
        -------
        Plasma angular frequency of electrons : 1/time Quantity

        Notes
        -----
        The plasma angular frequency of electrons is defined as follows

        .. math:: \omega_{pe} = \sqrt{\\frac{n_e e^2}{m_e \epsilon_0}}
        """
        dim = 'angular_frequency'
        ne  = self._lpi.target.material.electron.number_density()
        wpe = _np.sqrt((ne * _u.e**2)/(_u.m_e * _u.epsilon_0))
        
        return self.default.result('angular_frequency_plasma',wpe,dim)

class _PlasmaIon(_PelpiObject):
    """
    Plasma parameters about ions.
    """
    def __init__(self,LaserPlasmaInteraction):
        # No need to check input because this method is only called in _PlasmaParameters definition

        # Initialise default dict
        self.default = _Default(self)

        # Save reference to LaserPlasmaInteraction instance in a private variable
        self._lpi   = LaserPlasmaInteraction

    def angular_frequency_plasma(self):
        """
        Returns
        -------
        Plasma angular frequency of ions : 1/time Quantity

        Notes
        -----
        The plasma angular frequency of ions is defined as follows

        .. math:: \omega_{pi} = \sqrt{\\frac{Z^2 n_i e^2}{m_i \epsilon_0}}
        """
        dim = 'angular_frequency'
        ni  = self._lpi.target.material.ion.number_density()
        Z   = self._lpi.target.material.Z()
        mi  = self._lpi.target.material.atomic_mass()
        wpi = _np.sqrt((ni * (Z * _u.e)**2)/(mi * _u.epsilon_0))
        
        return self.default.result('angular_frequency_plasma',wpi,dim)
