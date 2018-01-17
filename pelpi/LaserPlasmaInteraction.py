#coding:utf8

import numpy as _np
from . import unit as _u
from . import prefered_unit as _pu
from . import Model as _m

################################################################################
class LaserPlasmaInteraction(object):
    """
    Class for estimations in laser-plasma interaction.

    Pour le moment short pulse UHI et cible solide.

    No interaction/no propagation / propagation ?

    Par défaut :
        Calcul de tous les attributs ? Chiant mais plus pratique pour interaction avec
        les autres objets (ParticleInCell par ex.) -> ou alors faire des get dans ParticleInCell
        Calcul ajout des attributs lorsque calculés via get... ? -> tester si existant
        dans getInfo() pour affichage et paramètre pour return ?
        Calcul de presque rien par défaut ? -> plus simple.


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

    absorption, object
    A sub-class containing all the absorption processes implemented yet for laser-plasma interaction.

    ne_over_nc, float
    Electron density normalized to critical density

    ni_over_nc, float
    Ion density normalized to critical density

    Available Methods
    ================
    For extended documentation, refer to the desired method.

    General Methods
    --------------
    updateParameters()
    getInfo()

    About Laser
    ----------
    getLaserAbsorptionEfficiency

    About Target
    -----------
    getTargetConductivity      ###

    About Interaction
    -------------------------------
    lengthInteractionMax     ### fonction générique pour récupérer le max d'une méthode ? genre boucler sur tous les modèles
    timeInteractionMax

    getInteractionDominant # a priori cette interaction est la plus importante

    About Electrons
    --------------
    numberTotal(model, **kwargs)
    lengthCaracDepth
    temperature
    getHotElectronRMS
    getHotElectronEnergyLossTime
    getHotElectronAngularScatteringTime

    getColdElectronTemperature ## a trouver ?

    About Ions
    ---------
    getIonEnergyCutoff

    About Photons
    ------------



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

        self.updateParameters()

    def updateParameters(self):
        self.plasma     = PlasmaParameters(self)
        self.absorption = []
        self.model      = _m.Model
        self.electron   = self.Electron(self)
        # self.ion        = Ion(self)


    def getLaserAbsorptionEfficiency(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Model=_m.Model.Obvious(self)
            out  = Model.getLaserAbsorptionEfficiency()
        else:
            raise NameError("getLaserAbsorptionEfficiency : Unknown model name.")

        out.to_base_units()
        return out


    def getTargetConductivity(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Tec     = 1e-3
            logCoulomb = 5.
            Model=_m.Model.Obvious(self)
            self.Sigma  = Model.getTargetConductivity(Tec=Tec,logCoulomb=logCoulomb)
        else:
            raise NameError("getTargetConductivity : Unknown model name.")

        return self.Sigma


    class Electron(object):
        """

        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction
            self.hot    = self.Hot(self._lpi)
            # self.cold   = self.Cold(self._lpi)

        # TODO: here general stuff about all the electrons

        class Hot(object):
            """
            In UHI, super thermal electrons
            """
            def __init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction
                self.default_model={'numberTotal':'Bell1997','temperature':'Haines2009'}

            def numberTotal(self,model=None,**kwargs):
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
                # if model is None:
                #     model=self._lpi.default_model[model]
                #
                # if model in available_models:
                #    Model=_m.model # TODO: how to do this ?
                #
                #    Model.needed_models # TODO: do something like this for giving default behaviour
                #
                #     Model.checkHypotheses()
                #     return Model.numberTotal(**kwargs).to('dimensionless') # TODO: with this, need to put default behaviour into Model.py
                # else:
                #     raise NameError("Unknown model name.")


                # available_models=["Bell1997","Obvious"]
                # TODO: argument loop=True -> loop over all the models with a checkHypotheses and try, except for getting the max value for ex. (func=max in arguments and return func(list))
                # TODO: generic procedure : testing if in available_models and generic checkHypotheses + return model(**kwargs) ?
                if model=="Bell1997":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
                    nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
                    Model   = _m.Model.Bell1997(self)
                    Model.checkHypotheses()
                    nehTot = Model.numberTotal(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet
                elif model=="Obvious":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Model=_m.Model.Obvious(self)
                    nehTot = Model.numberTotal(Teh)
                else:
                    raise NameError("Unknown model name.")

                return nehTot

            def lengthCaracDepth(self,model="Bell1997",**kwargs):
                """
                """
                if model=="Bell1997":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
                    nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
                    Model   = _m.Model.Bell1997(self)
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

                if model in available_models:
                    Model=_m.Model.__dict__.get(model)(self._lpi)

                    Model.checkHypotheses()
                    return Model.getHotElectronTemperature(**kwargs).to(_pu[dim])
                else:
                    raise NameError("Unknown model name.")


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


    def updateParameters(self):
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
