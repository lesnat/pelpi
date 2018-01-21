#coding:utf8

# import numpy as _np
# from . import unit as _u
# from . import prefered_unit as _pu
from ._global import *
from ._tools import _Estimate
from .Model import LaserPlasmaInteraction as _m

__all__ = ["LaserPlasmaInteraction"]

################################################################################
class LaserPlasmaInteraction(object):
    """
    Class for estimations in laser-plasma interaction.

    Parameters
    ==========
    This class needs to be implemented with a laser object and a target object
    as arguments. Those classes could then be find as a sub-module.

    Class Attributes
    ================
    laser, object
    The Laser object given as argument when the class was declared.

    target, object
    The Target object given as argument when the class was declared.

    plasma, object
    A sub-class containing usual plasma parameters.


    Available Methods
    =================
    For extended documentation, refer to the desired method.

    General Methods
    --------------


    Use of arguments (*args) in methods
    ===================================
    Some models may need optional parameters, such as electron hot temperature
    or laser absorption efficiency for complete the calculus.
    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.
    Please refer to the method documentation for more informations.


    Examples
    ========
    >>> ...

    For complex models, see the documentation of modules,
    in pelpi.Model.LaserPlasmaInteraction

    Assuming lpi is an instanciated LaserPlasmaInteraction object :

    >>> eh  = lpi.electron.hot
    >>> Teh = eh.temperature(model="Wilks1992")
    >>> S   = lpi.target.conductivity(model=)
    >>> nu  = lpi.laser.efficiencyAbsorption(model=)

    Use models

    >>> neh_Bell = eh.numberDensity(
            model="Bell1997",
            temperature=Teh,
            conductivity=S,
            absorption_efficiency=nu)
    >>> neh_Common = eh.numberDensity(
            model="Common",
            absorption_efficiency=nu)

    Then print results

    >>> print("Estimated hot electron density :")
    >>> print("-----------------------------------------")
    >>> print("Bell1997     : neh = "+str(neh_Bell))
    >>> print("Common      : neh = "+str(neh_Obvious))
    >>> print("-----------------------------------------")

    """
    def __init__(self,Laser,Target):
        self.laser      = Laser
        self.target     = Target

        self.plasma     = PlasmaParameters(self)
        self.absorption = []
        self.model      = _m
        self.electron   = _Electron(self)
        # self.ion        = Ion(self)

class _Laser(object):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction

        # Automatically add all new methods to laser object
        # for model in self.__dict__.keys():
        #     _addMethod(self._lpi.laser, self, model)

        self._lpi.laser.efficiencyAbsorption = self.efficiencyAbsorption

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


class _Target(object):
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

class _Electron(object):
    """

    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction
        self.hot    = self._Hot(self._lpi)
        # self.cold   = self.Cold(self._lpi)

    # TODO: here general stuff about all the electrons

    class _Hot(object):
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


        def lengthCaracDepth(self,model,*args):
            """
            Return an estimate of the characteristic penetration depth of
            hot electrons in the target.

            Arguments
            --------
            model, string
                Model name
            *args,
                Model input parameters

            Models
            -----
            Bell1997, a theoretical model taking into account the effects of
            the hot electron return current.
                Input parameters : temperature, conductivity, absorption_efficiency

            Notes
            ----
            See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
            if you need more informations about the [Model] model.
            """
            available_models=["Bell1997"]
            dim='length'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.use(method_name='electron_hot_lengthCaracDepth',dim=dim,*args)

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


        def timeInteractionMax(self,verbose=True):
            """
            """
            return 0.

        def lengthInteractionMax(self,verbose=True):
            return 0.


class PlasmaParameters(object):
    """
    Comment faire pour utiliser une température autre que Te_pond ?
    via meilleure estimation de la température si abso != JxB ou donner le choix ?
    Passer tout ca en méthodes ?
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi             = LaserPlasmaInteraction
        self.updateParameters()


    def updateParameters(self): # TODO; convert to methods
        self.wpe        = 0.0 # Electron plasma frequency
        self.wpi        = 0.0 # Ion plasma frequency
        self.lambda_De  = 0.0 # Debye length
        self.vTe        = 0.0 # Electron thermal velocity
        self.vTi        = 0.0 # Ion thermal velocity
        self.vA         = 0.0 # Alfven velocity
        self.EFermi     = 0.0

    def getInfo(self):
        txt  = ""

        return txt
