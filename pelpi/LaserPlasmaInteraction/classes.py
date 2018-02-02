#coding:utf8

from .._global import *
from .._tools import _Estimate,_PelpiObject
from ..LaserPlasmaInteraction import model as _m

__all__ = ["LaserPlasmaInteraction"]

################################################################################
class LaserPlasmaInteraction(_PelpiObject):
    """
    Class for estimations in laser-plasma interaction.

    Parameters
    ----------
    Laser : object
        Instanciated ``pelpi.Laser`` object
    Target : object
        Instanciated ``pelpi.Target`` object

    Attributes
    ----------
    laser : sub-module
        The ``pelpi.Laser`` object given as argument when the class was declared.
    target : sub-module
        The ``pelpi.Target`` object given as argument when the class was declared.
    plasma : sub-module
        Contains usual plasma parameters.
    model : sub-module
        Contains the all the available models.

    Notes
    -----
    Use of arguments (*args) in methods
    +++++++++++++++++++++++++++++++++++
    Some models may need optional parameters, such as electron hot temperature
    or laser absorption efficiency for complete the calculus.
    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.
    Please refer to the method documentation for more informations.


    Examples
    --------
    Assuming you instanciated a ``pelpi.Target`` object as ``targ``
    and a ``pelpi.Laser`` object as ``las``,
    you can instanciate the ``pelpi.LaserPlasmaInteraction`` object as follows :

    >>> import pelpi as pp
    >>> lpi = pp.LaserPlasmaInteraction(las,tar)

    and can still access to ``targ`` and ``las`` properties from ``lpi`` object.

    >>> print("Laser normalized peak intensity : {}".format(lpi.laser.intensityPeakNormalized()))

    A list of available models for each estimate can be found in the method documentation.

    >>> help(lpi.electron.hot.temperature)

    Once you choose one that corresponds to your case, you can get more informations about it

    >>> help(lpi.model.Beg1997)

    get an estimate (here the supra-thermal electron temperature from the Beg1997 model)

    >>> eh  = lpi.electron.hot
    >>> Teh = eh.temperature(model="Beg1997")

    and use the estimate for other calculations,
    like the corresponding normalized Maxwell-Boltzmann distribution.

    >>> Ek = np.linspace(0.1,10,100) * pp.unit('MeV')
    >>> MB = lpi.model.Common.distribution("MB",kinetic_energy=Ek,temperature=Teh)

    You can build more and more complex estimations,

    >>> S   = lpi.target.conductivity(model=)
    >>> nu  = lpi.laser.efficiencyAbsorption(model=)
    >>> neh_Bell = eh.numberDensity(
            model="Bell1997",
            temperature=Teh,
            conductivity=S,
            absorption_efficiency=nu)
    >>> neh_Common = eh.numberDensity(
            model="Common",
            absorption_efficiency=nu)

    and compare the different results with your experimental or simulation results.

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> Ek_sim, Spec_sim = np.loadtxt("spectrum.txt").T
    >>> plt.plot(Ek_sim,Spec_sim,"Simulation results")
    >>> plt.plot(Ek,neh_Bell*MB,label="MB 'Beg1997' estimate with 'Bell1997' normalisation")
    >>> plt.plot(Ek,neh_Common*MB,label="MB 'Beg1997' estimate with 'Common' normalisation")
    >>> plt.axes(xlabel='$E_k$ (MeV)',ylabel='Number of $e^-$ per MeV')
    >>> plt.legend()
    >>> plt.show()

    Thank to the 'all in method' structure, it is then possible to loop over one or more parameters
    to plot parametric evolution of an estimate with several models involved

    >>> tFWHM   = np.linspace(20,200,100)*pp.unit('fs')
    >>> neh     = []
    >>> for t in tFWHM:
    ...     lpi.laser.set(time_fwhm=t)
    ...     Teh = eh.temperature(model='Haines2009')
    ...     S   =
    ...     nu  =
    ...     neh.append()
    ...
    >>> plt.figure()
    >>> plt.plot(tFWHM,neh)
    >>> plt.axes(xlabel='Pulse temporal FWHM (fs)',ylabel='Total number of hot electrons')
    >>> plt.show()
    """

    model      = _m # public attribute

    def __init__(self,Laser,Target):
        self.laser      = Laser
        self.target     = Target
        self.plasma     = _PlasmaParameters(self)
        self.electron   = _Electron(self)
        # self.ion        = Ion(self)


class _Laser(_PelpiObject):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction

        self._user_values=self._lpi.laser._user_values

        exclude=['set_default','get_default']
        for var in dict(self._lpi.laser):
            if var[0]!='_' and var not in exclude:
                self.__dict__[var]=getattr(self._lpi.laser,var)

        self._setMethodsToDict()

        # Automatically add all new methods to laser object
        # for model in self.__dict__.keys():
        #     _addMethod(self._lpi.laser, self, model)

        # self._lpi.laser.efficiencyAbsorption = self.efficiencyAbsorption

    def efficiencyAbsorption(self,model,*args): # TODO: what this model is about ? hot electrons ? ions ? ...
        """
        Return an estimate of the laser absorption efficiency into hot electrons ??.

        Arguments
        --------
        model, string
            Model name
        *args,
            Model input parameters

        Models
        -----
        Common, a theoretical model for a rough estimate.
            Input parameters : ...

        Notes
        ----
        See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
        if you need more informations about the [Model] model.
        """
        available_models=["Common"]
        dim='number'

        estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
        return estimate.use(method_name='laser_efficiencyAbsorption',dim=dim,*args)


class _Target(_PelpiObject):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction

        # Automatically add all new methods to laser object
        # for model in self.__dict__.keys():
        #     _addMethod(self._lpi.laser, self, model)

        self._lpi.target.conductivity = self.conductivity

        # add targetdensitynormalized


    def conductivity(self,model,args):
        """
        Return an estimate of the target electric conductivity.

        Arguments
        --------
        model, string
            Model name
        *args,
            Model input parameters

        Models
        -----
        Common, a theoretical model for a rough estimate.
            Input parameters : ...

        Notes
        ----
        See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
        if you need more informations about the [Model] model.
        """
        available_models=["Common"]
        dim='conductivity'

        estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
        return estimate.use(method_name='target_conductivity',dim=dim,*args)

class _Electron(_PelpiObject):
    """

    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction
        self.hot    = self._Hot(self._lpi)
        # self.cold   = self.Cold(self._lpi)

    # TODO: here general stuff about all the electrons
    # TODO: add number density ?

    class _Hot(_PelpiObject):
        """
        In UHI, super thermal electrons
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi = LaserPlasmaInteraction

        def numberTotal(self,model,*args):
            """
            Return an estimate of the total hot electron number.

            Arguments
            --------
            model, string
                Model name
            *args,
                Model input parameters

            Models
            -----
            Common, a theoretical model for a rough estimate.
                Input parameters : ...

            Notes
            ----
            See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
            if you need more informations about the [Model] model.
            """
            available_models=["Common"]
            dim='number'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.use(method_name='electron_hot_numberTotal',dim=dim,*args)

        def temperature(self,model,*args):
            """
            Return an estimate of the hot electron temperature.

            Arguments
            --------
            model, string
                Model name
            *args,
                Model input parameters

            Models
            -----
            Beg1997, an empirical model ...
                Input parameters : None

            Haines2009, a theoretical model ...
                Input parameters : None

            Wilks1992, a theoretical model
                Input parameters : None

            Notes
            ----
            See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
            if you need more informations about the [Model] model.
            """
            dim='temperature'
            available_models=["Beg1997","Haines2009","Wilks1992"]

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.use(method_name='electron_hot_temperature',dim='temperature',*args)


class _PlasmaParameters(_PelpiObject):
    """
    Comment faire pour utiliser une température autre que Te_pond ?
    via meilleure estimation de la température si abso != JxB ou donner le choix ?
    Passer tout ca en méthodes ?
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi             = LaserPlasmaInteraction


    # def updateParameters(self): # TODO; convert to methods
    #     self.wpe        = 0.0 # Electron plasma frequency
    #     self.wpi        = 0.0 # Ion plasma frequency
    #     self.lambda_De  = 0.0 # Debye length
    #     self.vTe        = 0.0 # Electron thermal velocity
    #     self.vTi        = 0.0 # Ion thermal velocity
    #     self.vA         = 0.0 # Alfven velocity
    #     self.EFermi     = 0.0
    #
    #
    def electronLengthDebye(self,temperature):
        """
        Returns
        -------
        Debye length of electrons : length quantity

        Notes
        -----
        The Debye length is defined as

        .. math:: \lambda_{De} = \sqrt{\\frac{\epsilon_0 T_e}{n_e e^2}}
        """
        ne  = self._lpi.target.material.electronNumberDensity()
        Te  = temperature

        return _np.sqrt((_u.epsilon_0 * Te)/(ne * _u.e**2)).to(_pu['length'])


    def electronLengthLandau(self,temperature):
        """
        Returns
        -------
        Landau length of electrons : length quantity

        Notes
        -----
        The Landau length is defined as

        .. math:: r_0 = \\frac{e^2}{4 \pi \epsilon_0 T_e}
        """
        Te  = temperature

        return ((_u.e**2)/(4*_np.pi * _u.epsilon_0 * Te)).to(_pu['temperature'])

    def electronPulsationPlasma(self,temperature):
        """
        Returns
        -------
        Plasma pulsation of electrons : 1/time quantity

        Notes
        -----
        The Landau length is defined as

        .. math:: \omega_{pe} = \sqrt{\\frac{n_e e^2}{m_e \epsilon_0}}
        """
        ne  = self._lpi.target.material.electronNumberDensity()

        return _np.sqrt((ne * _u.e**2)/(_u.m_e * _u.epsilon_0))

    def ionPulsationPlasma(self):
        """
        Returns
        -------
        Plasma pulsation of ions : 1/time quantity

        Notes
        -----
        The Landau length is defined as

        .. math:: \omega_{pe} = \sqrt{\\frac{Z^2 n_i e^2}{m_i \epsilon_0}}
        """
        ni  = self._lpi.target.material.ionNumberDensity()
        Z   = self._lpi.target.material.Z # TODO: Change to method
        N   = self._lpi.target.material.N
        mi  = Z * _u.m_p + N * _u.m_n

        return _np.sqrt((ni * Z**2 * _u.e**2)/(mi * _u.epsilon_0))
