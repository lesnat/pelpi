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

    Pour le moment short pulse UHI et cible solide.

    No interaction/no propagation / propagation ?

    Arguments
    ========
    This class needs to be implemented with a laser object and a target object
    as arguments. Those classes could then be find as a class sub-object.

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


    Use of keyword arguments (kwargs) in methods
    ===========================================
    Some models may need optional parameters, such as electron hot temperature
    or laser absorption efficiency for complete the calculus.
    These parameters can be calculated by other models, whose can be choosen
    by setting the parameter model as a keyword argument.
    If you want to use a model with your own parameters,
    please do this by using directly the desired object.

    Example
    -------
    ``
    lpi.electron.hot.numberTotal(model="Bell1997", Teh_model="Wilks1992")
    ``
    is equivalent to
    ``
    T   = lpi.temperature(model="Wilks1992")
    S   = lpi.getTargetConductivity()
    nu  = lpi.getLaserAbsorptionEfficiency()
    Bell1997(lpi).numberTotal(Teh=T,Sigma=S,nu_laser=nu)
    ``

    Here the numberTotal method is call,
    specifying the desired model for the calculus as "Bell1997".
    Because this model needs a temperature (and other parameters)
    for complete the calculus, it is possible to change the parameter model used
    for hot electron temperature by setting the keyword argument
    Teh_model to "Wilks1992" for example.
    Available parameter models can be found in the documentation
    of desired parameter (here in the temperature method documentation).
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

    def efficiencyAbsorption(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Model=_m.Obvious(self)
            out  = Model.getLaserAbsorptionEfficiency()
        else:
            raise NameError("getLaserAbsorptionEfficiency : Unknown model name.")

        out.to_base_units()
        return out


class _Target(object):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi   = LaserPlasmaInteraction

        # Automatically add all new methods to laser object
        # for model in self.__dict__.keys():
        #     _addMethod(self._lpi.laser, self, model)

        self._lpi.target.conductivity = self.conductivity


    def conductivity(self,model="Obvious",**kwargs):
        """
        """

        available_models=["Obvious"]

        if type(model)!=str:
            raise TypeError("'model' type must be 'string', but it is "+ type(model))

        if model=="Obvious":
            Tec     = 1e-3
            logCoulomb = 5.
            Model=_m.Obvious(self)
            self.Sigma  = Model.getTargetConductivity(Tec=Tec,logCoulomb=logCoulomb)
        else:
            raise NameError("Model name given : "+model+", available are "+available_models)

        return self.Sigma


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
            self.default_model={'numberTotal':'Bell1997','temperature':'Haines2009'}

        def numberTotal(self,model=None,**kwargs):
            # TODO: delete Bell1997 because it is ne * surface_l * z0
            # TODO: -> too many models & hypotheses. let the user choose.
            """
            Return the total number of accelerated hot electrons [dimensionless].

            # Dimension
            # --------
            # dimensionless

            Arguments
            --------
            model, string (optional, default : "Bell1997")
            Name of the model.

            **kwargs, string(s)
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
            return estimate.use(method_name='electron_hot_numberTotal',dim=dim,**kwargs)


        def lengthCaracDepth(self,model="Bell1997",**kwargs):
            """
            """
            if model=="Bell1997":
                Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
                nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
                Model   = _m.Bell1997(self)
                Model.checkHypotheses()
                zeh = Model.lengthCaracDepth(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet

            return zeh

        def temperature(self,model,**kwargs):
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
            return estimate.use(method_name='electron_hot_temperature',dim='temperature',**kwargs)


        def timeInteractionMax(self,verbose=True):
            """
            """
            return 0.

        def lengthInteractionMax(self,verbose=True):
            return 0.


################################################################################
# class Absorption(object):
#     def __init__(self,name):
#         self.name=name
#
#     def getInteractionTime(self,verbose):
#         self.InteractionTime = 1.
#         if verbose:
#             print(self.name+" interaction time : "+str(self.InteractionTime)+" s")
#         return self.InteractionTime
#
#     def getInteractionLength(self,verbose):
#         self.InteractionLength = self.getInteractionTime/unit.c
#         if verbose:
#             print(self.name+" interaction length : "+str(self.InteractionLength)+" s")
#         return self.InteractionLength
#
# class Emmission(object):
#     def __init__(self,name):
#         self.name=name
#
# class JxB(Absorption):
#     def __init__(self):
#         pass
#
# class VacuumHeating(Absorption):
#     def __init__(self):
#         pass
#
# class Wakefield(Absorption):
#     def __init__(self):
#         pass

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
