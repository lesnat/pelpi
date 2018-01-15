#coding:utf8
import numpy as _np
from . import unit

################################################################################
"""
Malka 2001 -> Scaling Energie max electrons
"""
class Model(object): # TODO: Voire pour enlever classe Model mais avoir un sous-module Model
    class Beg1997(object):
        """
        Class for estimating ...
        Experimental fit

        ...
        Experimental laser intensity etc ...
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi         = LaserPlasmaInteraction # obligé de passer par self._lpi dans ce cas car appel de lpi hors de __init__, sinon variable privée _lpi par convention

        def checkHypotheses(self):
            pass

        def getHotElectronTemperature(self):
            """
            voire cold/hot temperature (ici hot)
            Tan et al. T_hot= 30 * I_17**(1/3) keV (ici 100)
            in keV
            """
            # return (100.*unit.keV/(511*unit.keV)) * (self._lpi.laser.I0.to(unit.W*unit.cm**-2)/(1e17*unit.W*unit.cm**-2) * (self._lpi.laser.wavelength.to(unit.um))**2 )**(1/3.)
            return (100.*unit.keV) * (self._lpi.laser.I0.to(unit.W*unit.cm**-2)/(1e17*unit.W*unit.cm**-2) * (self._lpi.laser.wavelength.to(unit.um)/(1*unit.um))**2 )**(1/3.)

        def getIonEnergyCutoff(self):
            """
            Return the maximum ion energy in me c**2,
            """
            return (1.2e-2/511) * (1e-4*self._lpi.laser.I0)**(0.313)

    class Bell1997(object):
        """
        Class for estimating ...
        Return current

        Attributes
        ---------
        n0, float
        Estimate of the number of accelerated electrons.

        z0, float
        Estimate of the penetration depth of fast electrons (distance from the surface).

        Methods
        ------
        checkHypotheses()
        getHotElectronTotalNumber()
        getHotElectronPenetrationDepth(model)

        Hypotheses
        ---------
        Short pulse (< 1 ps)
        High intensity (>10^18 W.cm^-2)
        Colisionless plasma
        Maxwellian electron distribution (ref ?)

        Constant conductivity in the plasma (laisser cette hyp ?)
        T0 constant during the laser pulse (colision time larger than interaction time)

        Reference
        --------
        A R Bell, J R Davies, S Guerin, H Ruhl,
        Fast-electron transport in high-intensity short-pulse laser-solid experiments,
        Plasma Phys. Control. Fusion, 1997.

        Notes
        ----


        """

        def __init__(self,LaserPlasmaInteraction): # A définir ici ou dans les méthodes ??? car certaines méthodes n'ont pas besoin de tous les param
            self._lpi        = LaserPlasmaInteraction

        def checkHypotheses(self,verbose=0):
            """
            Method for verifying hypotheses of the model.

            Arguments
            --------
            verbose, int (optional, default : 0)

            """
            # if verbose==0:
            #     print "Detailled informations"
            # if verbose==1:
            #     print "Warnings about models"
            # if verbose==2:
            #     print "Only warnings about parameters"
            # if verbose==3:
            #     print "Nothing."
            pass

        def getHotElectronDensity(self,Teh,Sigma,nu_laser,t=0.0,z=0.0):
            n0 = (2 * (nu_laser*self._lpi.laser.I0)**2 * self._lpi.laser.getTimeIntegral())/(9 * unit.e * (Teh / unit.e)**3 * Sigma)
            z0 = self.getHotElectronPenetrationDepth(Teh,Sigma,nu_laser) # ,t ?
            # return n0 * (t/self._lpi.laser.getTimeIntegral()) * (z0/(z+z0))**2
            return n0

        def getHotElectronTotalNumber(self,Teh,Sigma,nu_laser): # a déplacer dans lpi ? car pas forcemment z0 en longi
            return self.getHotElectronDensity(Teh,Sigma,nu_laser,t=0.0*unit.s,z=0.0*unit.m)*\
                self.getHotElectronPenetrationDepth(Teh,Sigma,nu_laser,t=0.0*unit.s)*\
                self._lpi.laser.getSurfaceIntegral()

        def getHotElectronPenetrationDepth(self,Teh,Sigma,nu_laser,t=0.0 * unit.s):
            """
            Return the estimate electron penetration depth
                - In the interaction time
                - After the interaction time (due to diffusion)

            Attributes
            ---------
            t, float (optional, default : 0.0)
            Time.
            """
            # if unit.Quantity.__lt__(t,self._lpi.laser.getTimeIntegral()):
            if t < self._lpi.laser.getTimeIntegral():
                return (3 * (Teh / unit.e)**2 * Sigma)/(nu_laser*self._lpi.laser.I0)
            else:
                return 1.78 * self.getHotElectronPenetrationDepth(t=0.0 *unit.s) * (t/self._lpi.laser.getTimeIntegral() - 0.618)**(3/5.)

        def plotElectronDensity(self):
            pass

    class Braginskii1965(object):
        """
        """
        def __init__(self):
            pass

        def getHotElectronPenetrationDepth(self):
            pass

        def getHotElectronEnergyLossTime(self):
            pass

        def getHotElectronAngularScatteringTime(self):
            pass

        def getHotElectronRMS(self):
            pass

        def getTargetConductivity(self):
            pass

    class Davies2003(object):
        """
        Theoretical paper on Electric and Magnetic field generation and target heating
        by laser-generated fast electrons + electrical conductivity.
        Change of resistivity due to Ohmic heating.


        Hypotheses
        ---------
        Material is a conductor
        Arbitrary power law of resistivity on temperature
        Electron current is fixed (rigid beam approximation)
        Charge diffusion is instantaneous
        Magnetic diffusion is negligible

        """
        def __init__(self,LaserPlasmaInteraction):
            lpi         = LaserPlasmaInteraction

    class Haines2009(object):
        """
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi         = LaserPlasmaInteraction

        def checkHypotheses(self):
            pass

        def getHotElectronTemperature(self):
            """
            Hot electron temperature in me c**2

            """
            return ((1.0 + 2.0**(1/2.) * self._lpi.laser.a0)**(1/2.) - 1.0) * 511 * unit.keV

    class Mora2003(object):
        """
        Theoretical paper on plasma expansion into vacuum, focused on ion acceleration
        and calculations of electric fields.

        1d, Maxwellian electron distribution (constant in time), sharp edge ...
        """
        def __init__(self,LaserPlasmaInteraction):
            lpi         = LaserPlasmaInteraction

        def checkHypotheses(self):
            pass

        def getInitialFrontElectricField(self,Te):
            """
            Return the electric field in the front (=edge ?) for initial time.
            """
            return _np.sqrt(2/_np.exp(1)) * (lpi.target.mat.ne * Te/unit.epsilon_0)**(1/2.)

        def getIonEnergyCutoff(self):
            pass

    class Wilks1992(object):
        """
        Class for estimating ...
        Based of the paper of Wilks, ..., 1992.

        Attributes
        ---------


        Methods
        ------



        Notes
        ----


        """

        def __init__(self,LaserPlasmaInteraction):
            self._lpi        = LaserPlasmaInteraction

        def checkHypotheses(self):
            pass

        def getHotElectronTemperature(self):
            return ((1.0 + self._lpi.laser.a0**2)**(1/2.) - 1.0 )*511 * unit.keV


    ################################################################################
    class Obvious(object):
        """
        Class containing obvious theoretical estimations, for order of magnitudes.
        It also contains commonly used functions, such as Maxwell-Boltzmann distribution,
        Spitzer conductivity, etc ... that would not be relevant to include in a dedicated
        object due to their old and massive use.

        Attributes
        ---------


        Methods
        ------



        Notes
        ----


        """

        def __init__(self,LaserPlasmaInteraction):
            self._lpi        = LaserPlasmaInteraction

        def getHotElectronTotalNumber(self,Teh):
            """

            .. math:
                \frac{E_{laser}}{3/2 k_b T_e^{hot}}
            """
            return self._lpi.laser.energy/(3/2. * Teh) # voire si changement d'unité de Teh

        def getTargetConductivity(self,Tec,logCoulomb): # getSpitzer ? getTargetConductivity ?
            """
            Spitzer conductivity.

            .. math :
                \frac{(4 \pi \epsilon_0)^2 (k_b T_e^{cold})^{3/2}}{\pi Z e^2 \sqrt{m_e} \ln(\Lambda)}
            """
            return (4*_np.pi*unit.epsilon_0)**2 * (Tec*unit.m_e*unit.c**2)**(3/2.) / (_np.pi*self._lpi.target.mat.Z * unit.e**2 * unit.m_e**(1/2.) * logCoulomb)

        def getLaserAbsorptionEfficiency(self):
            return unit.Quantity(0.5)
