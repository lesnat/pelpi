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

    Arguments
    ========
    This class needs to be implemented with a laser object and a target object
    as arguments. Those classes could then be find as a sub-module.

    Class Attributes
    ===============
    laser, object
    The Laser object given as argument when the class was declared.

    target, object
    The Target object given as argument when the class was declared.

    plasma, object
    A sub-class containing usual plasma parameters.


    Available Methods
    ================
    For extended documentation, refer to the desired method.

    General Methods
    --------------


    Use of arguments (*args) in methods
    ===========================================
    Some models may need optional parameters, such as electron hot temperature
    or laser absorption efficiency for complete the calculus.
    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.
    Please refer to the method documentation for more informations.


    Examples
    =======
    ``
    ( simple example )
    ``

    For complex models, see the documentation of modules,
    in pelpi.Model.LaserPlasmaInteraction

    ``
    (complex example)
    # assuming lpi is an instanciated LaserPlasmaInteraction object :

    eh  = lpi.electron.hot
    Teh = eh.temperature(model="Wilks1992")
    S   = lpi.target.conductivity(model=)
    nu  = lpi.laser.efficiencyAbsorption(model=)

    neh_Bell = eh.numberDensity(\
            model="Bell1997",\
            temperature=Teh,\
            conductivity=S,\
            absorption_efficiency=nu)

    neh_Obvious = eh.numberDensity(\
            model="Common",\
            absorption_efficiency=nu)


    print("Estimated hot electron density with different models :")
    print("-----------------------------------------")
    print("Bell1997     : neh = "+str(neh_Bell))
    print("Obvious      : neh = "+str(neh_Obvious))
    print("-----------------------------------------")
    ``
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

    def efficiencyAbsorption(self,model,*args):
        """
        """
        available_models=["Obvious"]
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


    def conductivity(self,model,args):
        """
        """
        available_models=["Obvious"]
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
            # TODO: delete Bell1997 because it is ne * surface_l * z0
            # TODO: -> too many models & hypotheses. let the user choose.
            """
            Return the total number of accelerated hot electrons [dimensionless].

            Arguments
            --------
            model, string
            Name of the model.

            *args, string(s)
            See "Parameter models" in section Models.
            For more informations about keyword arguments please refer to
            the documentation of the LaserPlasmaInteraction object.

            Models
            -----
            Bell1997 is a model created for ...
            Need a (hot electron?) temperature, electrical conductivity and laser absorption
            efficiency to work properly.
            Parameter models :
                for the hot electron temperature : Teh_model (default : "Haines2009")
                for conductivity : Sigma_model (default : "Obvious", i.e. Spitzer)
                for absorption efficiency nu_laser_model (default : "...")

            Obvious is a simple estimation, for order of magnitude.
            It returns the total laser energy over the energy in hot electrons,
            estimate by 3/2 Teh.
            It needs a hot electron temperature to work properly.
            Parameter models :
                for the hot electron temperature : Teh_model (default : "Haines2009")

            Examples
            -------
            n0 = lpi.electron.hot.numberTotal(model="Obvious")
            n0 = lpi.electron.hot.numberTotal(model="Bell1997", Teh_model="Wilks1992")
            """
            available_models=["Bell1997","Obvious"]
            dim='number'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.use(method_name='electron_hot_numberTotal',dim=dim,*args)


        def lengthCaracDepth(self,model,*args):
            """
            """
            available_models=["Bell1997"]
            dim='length'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.use(method_name='electron_hot_lengthCaracDepth',dim=dim,*args)

        def temperature(self,model,*args):
            """
            Return the hot electron temperature.

            Arguments
            --------
            model, string
            Name of the model.

            Models
            -----
            Beg1997 is an empirical model ...
            Based on the reference

            Haines2009 is a theoretical model ...
            Based on the reference

            Wilks1992 is an empirical model
            Based on the reference
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
