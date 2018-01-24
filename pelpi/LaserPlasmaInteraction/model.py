#coding:utf8
# import numpy as _np
# from .. import unit as _u
from .._global import *
from .._tools import _Model
################################################################################
"""
Malka 2001 -> Scaling Energie max electrons
"""

class Beg1997(_Model):
    """
    Class for estimating ...
    Experimental fit

    hypotheses

    reference
    ...
    Experimental laser intensity etc ...
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi         = LaserPlasmaInteraction

    def checkHypotheses(self):
        """
        Check the hypotheses of the model.

        Warnings can be configured in pelpi.warnings.filterwarnings method.
        """
        if self._lpi.laser.intensity()>1*_u('W/cm**2'):
            _w.warn('Test warning because tatata')

    def electron_hot_temperature(self): # TODO: change by sub-class Electron sub-class Hot method temperature ?
        """
        Return an estimate of the hot electron temperature from the Beg1997 model.

        .. math:
            T_e^h = 100 * (\\frac{I_{17} \lambda_{\mu}^2})^(1/3)
            with $T_e^h$ the hot electron temperature in keV
            $I_{17}$ the laser peak intensity in $10^{17} W.cm^{-2}$
            $\lambda_{\mu}$ the laser wavelength in $10^{-6}$ m
        """
        I0              = self._lpi.laser.intensity()
        lambda_laser    = self._lpi.laser.wavelength()

        Te = 100.*_u('keV') * ((I0 * lambda_laser**2) / (1e17*_u('W/cm**2')*_u('um**2')) )**(1/3.)

        return Te.to(_pu['temperature'])

    def ion_energyCutoff(self):
        """
        Return the maximum ion energy in me c**2,
        """
        return (1.2e-2*_u('keV')) * (self._lpi.laser.I0.to('W/cm**2'))**(0.313)


class Bell1997(_Model):
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
    electron_hot_numberTotal()
    electron_hot_lengthCaracDepth()

    Hypotheses
    ---------
    Short pulse (< 1 ps)
    High intensity (>10^18 W.cm^-2)
    Colisionless plasma
    Maxwellian hot electron distribution
    Constant conductivity in the plasma
    T0 constant during the laser pulse (collision time larger than interaction time)

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

    def checkHypotheses(self):
        """
        Check the hypotheses of the model.

        Warnings can be configured in pelpi.warnings.filterwarnings method.
        """
        if self._lpi.laser.profile.timeIntegral()>1*_u('ps'): # TODO: maybe change by timeCarac()
            _w.warn('Pulse duration > 1 ps')
        if self._lpi.laser.intensity()<10**18 *_u('W/cm**2'):
            _w.warn('Laser peak intensity < 10**18 W/cm**2')
        # if self._lpi.plasma.collisionRate()>1e-3 * _u(''):
        #     _w.warn('Plasma collision rate > 1e-3')
        # if not self._lpi.electron.hot.isMaxwellian():
        #     _w.warn('Electron not follow Maxwell-Boltzmann distribution')

        # _w.warn('Conductivity is assumed to be constant in the plasma')
        # _w.warn('Electron hot temperature is assumed to be constant during the laser pulse')

    def electron_hot_numberDensity(self,temperature_hot,conductivity,absorption_efficiency,t=0.0,z=0.0):
        Teh = temperature_hot
        Sigma = conductivity
        eta_l = absorption_efficiency

        n0 = (2 * (eta_l*self._lpi.laser.I0)**2 * self._lpi.laser.getTimeIntegral())/(9 * _u.e * (Teh / _u.e)**3 * Sigma)
        z0 = self.electron_hot_lengthCaracDepth(Teh,Sigma,eta_l) # ,t ?
        # return n0 * (t/self._lpi.laser.getTimeIntegral()) * (z0/(z+z0))**2
        return n0

    def electron_hot_lengthCaracDepth(self,temperature_hot,conductivity,absorption_efficiency,t=0.0 * _u.s):
        """
        Return the estimate electron penetration depth
            - In the interaction time
            - After the interaction time (due to diffusion)

        Attributes
        ---------
        t, float (optional, default : 0.0)
            Time.
        """
        # if _u.Quantity.__lt__(t,self._lpi.laser.getTimeIntegral()):
        Teh = temperature_hot
        Sigma = conductivity
        eta_l = absorption_efficiency

        if t < self._lpi.laser.getTimeIntegral():
            return (3 * (Teh / _u.e)**2 * Sigma)/(nu_laser*self._lpi.laser.I0)
        else:
            return 1.78 * self.electron_hot_lengthCaracDepth(t=0.0 *_u.s) * (t/self._lpi.laser.getTimeIntegral() - 0.618)**(3/5.)

    def electron_density(self):
        pass

class Braginskii1965(_Model):
    """
    """
    def __init__(self):
        pass

    def electron_hot_lengthCaracDepth(self):
        pass

    def electron_hot_timeEnergyLoss(self):
        pass

    def electron_hot_timeAngularScattering(self):
        pass

    def electron_hot_RMS(self):
        pass

    def target_conductivity(self):
        pass

class Davies2003(_Model):
    """
    Theoretical paper on Electric and Magnetic field generation and target heating
    by laser-generated fast electrons + electrical conductivity.
    Change of resistivity due to Ohmic heating.


    Hypotheses
    ----------
    Material is a conductor
    Arbitrary power law of resistivity on temperature
    Electron current is fixed (rigid beam approximation)
    Charge diffusion is instantaneous
    Magnetic diffusion is negligible

    """
    def __init__(self,LaserPlasmaInteraction):
        lpi         = LaserPlasmaInteraction

class Haines2009(_Model):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi         = LaserPlasmaInteraction

    def checkHypotheses(self):
        """
        Check the hypotheses of the model.

        Warnings can be configured in pelpi.warnings.filterwarnings method.
        """
        if self._lpi.laser.intensity()>1*_u('W/cm**2'):
            _w.warn('Test warning because tatata',UserWarning)

    def electron_hot_temperature(self):
        """
        Return an estimate of the hot electron temperature from the Haines2009 model.

        .. math:
            T_e^h = (\sqrt{1 + \sqrt{2} \ a_0} - 1 ) m_e c^2
            with $T_e^h$ the hot electron temperature
            $a_0$ the normalized laser intensity
            $m_e c^2$ the electron mass energy
        """
        a0 = self._lpi.laser.intensityPeakNormalized()
        return ((1.0 + 2.0**(1/2.) * a0)**(1/2.) - 1.0) * 511 * _u('keV')

class Mora2003(_Model):
    """
    Theoretical paper on plasma expansion into vacuum, focused on ion acceleration
    and calculations of electric fields.

    1d, Maxwellian electron distribution (constant in time), sharp edge ...
    """
    def __init__(self,LaserPlasmaInteraction):
        lpi         = LaserPlasmaInteraction

    def checkHypotheses(self):
        """
        Check the hypotheses of the model.

        Warnings can be configured in pelpi.warnings.filterwarnings method.
        """
        if self._lpi.laser.intensity()>1*_u('W/cm**2'):
            _w.warn('Test warning because tatata',UserWarning)

    def getInitialFrontElectricField(self,Te): # TODO: change the name + which temperature ??
        """
        Return the electric field in the front (=edge ?) for initial time.
        """
        return _np.sqrt(2/_np.exp(1)) * (lpi.target.mat.ne * Te/_u.epsilon_0)**(1/2.)

    def ion_energyCutoff(self):
        pass

class Wilks1992(_Model):
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
        """
        Check the hypotheses of the model.

        Warnings can be configured in pelpi.warnings.filterwarnings method.
        """
        if self._lpi.laser.intensity()>1*_u('W/cm**2'):
            _w.warn('Test warning because tatata',UserWarning)

    def electron_hot_temperature(self):
        """
        Return an estimate of the hot electron temperature from the Wilks1992 model.

        .. math:
            T_e^h = (\sqrt{1 + a_0^2} - 1 ) m_e c^2
            with $T_e^h$ the hot electron temperature
            $a_0$ the normalized laser intensity
            $m_e c^2$ the electron mass energy
        """
        a0 = self._lpi.laser.intensityPeakNormalized()
        return ((1.0 + (a0)**2)**(1/2.) - 1.0 ) * 511 * _u('keV') # TODO: a0 or a0/2 ?


################################################################################
class Common(_Model):
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

    def checkHypotheses(self):
        """
        Because this class is used for various features,
        the checkHypotheses method do nothing here.
        Hypotheses are checked in methods.
        """
        pass

    def electron_hot_numberTotal(self,temperature_hot,absorption_efficiency):
        """
        Return an estimate of the hot electron total number,
        based on the assumption that hot electron distribution is a Maxwellian.

        Parameters
        ---------
        temperature_hot, float
            Hot electron temperature
        absorption_efficiency, float
            Laser absorption efficiency into hot electrons

        .. math:
            n_0 = \\frac{\eta_{l} E_{l}}{3/2 T_e^{hot}}
            with $n_0$ the hot electron total number,
            $\eta_l$ the laser absorption efficiency into hot electrons,
            $E_l$ the laser total energy,
            $T_e^{hot}$ the thermal energy of hot electrons.
        """
        Teh = temperature_hot

        return (self._lpi.laser.energy/(3/2. * Teh)).to(_pu['number'])

    def target_conductivity(self,temperature_cold,log_coulomb):
        """
        Spitzer conductivity.

        .. math :
            \\frac{(4 \pi \epsilon_0)^2 (k_b T_e^{cold})^{3/2}}{\pi Z e^2 \sqrt{m_e} \ln(\Lambda)}
        """
        Tec = temperature_cold
        lnC = log_coulomb
        return (4*_np.pi*_u.epsilon_0)**2 * (Tec*_u.m_e*_u.c**2)**(3/2.) / (_np.pi*self._lpi.target.mat.Z * _u.e**2 * _u.m_e**(1/2.) * lnC)

    def laser_efficiencyAbsorption(self):
        return _u.Quantity(0.5)

    def electron_distribution(self,distribution,kinetic_energy,temperature):
        """

        """
        available=["MB"]
        Ek = kinetic_energy
        Te = temperature

        if name=="MB":
            return _np.sqrt(4/pi) * _np.sqrt(Ek/Te**3) * _np.exp( -Ek/Te )
        else:
            if type(distribution)!=str:
                raise TypeError("'distribution' type must be 'string', but it is "+str(type(distribution)))

            raise NameError("Distribution name "+distribution+" not found. Available are "+str(available))
