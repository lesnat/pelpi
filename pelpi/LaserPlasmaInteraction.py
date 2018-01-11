#coding:utf8

import numpy as _np
from __init__ import unit as _u
from __init__ import prefered_unit as _pu
import Model as _m

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
    getInteractionLengthMax     ### fonction générique pour récupérer le max d'une méthode ? genre boucler sur tous les modèles
    getInteractionTimeMax

    getInteractionDominant # a priori cette interaction est la plus importante

    About Electrons
    --------------
    getHotElectronTotalNumber(model, **kwargs)
    getHotElectronPenetrationDepth
    getHotElectronTemperature
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
    lpi.getHotElectronTotalNumber(model="Bell1997", Teh_model="Wilks1992")
    ``
    is equivalent to
    ``
    T   = lpi.getHotElectronTemperature(model="Wilks1992")
    S   = lpi.getTargetConductivity()
    nu  = lpi.getLaserAbsorptionEfficiency()
    Bell1997(lpi).getHotElectronTotalNumber(Teh=T,Sigma=S,nu_laser=nu)
    ``

    Here the getHotElectronTotalNumber method is call,
    specifying the desired model for the calculus as "Bell1997".
    Because this model needs a temperature (and other parameters)
    for complete the calculus, it is possible to change the parameter model used
    for hot electron temperature by setting the keyword argument
    Teh_model to "Wilks1992" for example.
    Available parameter models can be found in the documentation
    of desired parameter (here in the getHotElectronTemperature method documentation).
    """
    def __init__(self,Laser,Target):
        self.laser      = Laser
        self.target     = Target

        self.updateParameters()

    def updateParameters(self):
        self.plasma     = PlasmaParameters(self)
        self.absorption = []
        self.ne_over_nc = self.target.mat.ne/self.laser.nc
        self.ni_over_nc = self.target.mat.ni/self.laser.nc

        # a calculer à tous les coups ?
        # self.Teh        = self.getHotElectronTemperature()
        # self.Tec        = 0.

    def getInfo(self):
        txt  = " \n"
        txt += " Laser-plasma interaction :\n"
        txt += " ########################################## \n"
        txt += " Parameters :\n"
        txt += " ------------------------------------------ \n"
        txt += " ni/nc              :      "+str(self.ni_over_nc.to_base_units())+" \n"
        txt += " ne/nc              :      "+str(self.ne_over_nc.to_base_units())+" \n"
        txt += " \n"
        txt += " Predimonant absorption effects :\n"
        txt += " ------------------------------------------ \n"
        txt += " \n"
        txt += " Estimations :\n"
        txt += " ------------------------------------------ \n"

        # if self.target.mat.ne>self.laser.nc:


        txt += " ########################################## \n"
        return txt

    def getLaserAbsorptionEfficiency(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Model=_m.Obvious(self)
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
            Model=_m.Obvious(self)
            self.Sigma  = Model.getTargetConductivity(Tec=Tec,logCoulomb=logCoulomb)
        else:
            raise NameError("getTargetConductivity : Unknown model name.")

        return self.Sigma

    def getInteractionTimeMax(self,verbose=True):
        """
        """
        return 0.

    def getInteractionLengthMax(self,verbose=True):
        return 0.

    def getHotElectronTotalNumber(self,model="Bell1997",**kwargs):
        """
        Return the total number of accelerated electrons.

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
        n0 = lpi.getHotElectronTotalNumber(model="Obvious")
        n0 = lpi.getHotElectronTotalNumber(model="Bell1997", Teh_model="Wilks1992")
        """
        if model=="Bell1997":
            Teh     = self.getHotElectronTemperature(kwargs.get('Teh_model','Haines2009'))
            Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
            nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
            Model   = _m.Bell1997(self)
            Model.checkHypotheses()
            nehTot = Model.getHotElectronTotalNumber(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet
        elif model=="Obvious":
            Teh     = self.getHotElectronTemperature(kwargs.get('Teh_model','Haines2009'))
            Model=_m.Obvious(self)
            nehTot = Model.getHotElectronTotalNumber(Teh)
        else:
            raise NameError("Unknown model name.")

        return nehTot

    def getHotElectronPenetrationDepth(self,model="Bell1997",**kwargs):
        """
        """
        if model=="Bell1997":
            Teh     = self.getHotElectronTemperature(kwargs.get('Teh_model','Haines2009'))
            Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
            nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
            Model   = _m.Bell1997(self)
            Model.checkHypotheses()
            zeh = Model.getHotElectronPenetrationDepth(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet

        return zeh

    def getHotElectronTemperature(self,model="Haines2009"):
        """
        Return the hot electron temperature.

        Arguments
        --------
        model, string (optional, default : "Haines2009")
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

        if model=="Beg1997":
            Model=_m.Beg1997(self)
            # Model.checkHypotheses()
            out = Model.getHotElectronTemperature()
        elif model=="Haines2009":
            Model=_m.Haines2009(self)
            out = Model.getHotElectronTemperature()
        elif model=="Wilks1992":
            Model=_m.Wilks1992(self)
            out = Model.getHotElectronTemperature()
        else:
            raise NameError("Unknown model name. Please refer to the documentation.")

        return out.to(_pu['temperature'])


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
