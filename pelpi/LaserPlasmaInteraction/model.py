#coding:utf8
# import numpy as _np
# from .. import unit as _u
from .._global import *
from .._tools import _PelpiObject
################################################################################
"""
Malka 2001 -> Scaling Energie max electrons
"""

class Beg1997(_PelpiObject):
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

    def electron_hot_temperature(self):
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

        return Te.to(_du['temperature'])

    def ion_energy_cutoff(self):
        """
        Return the maximum ion energy
        """
        return (1.2e-2*_u('keV')) * (self._lpi.laser.I0.to('W/cm**2'))**(0.313)

# class Haines2009(_PelpiObject):
#     """
#     """
#     def __init__(self,LaserPlasmaInteraction):
#         global _lpi
#         _lpi = LaserPlasmaInteraction
#         # self._lpi       = LaserPlasmaInteraction
#         # self.electron   = self._Electron(self._lpi)
#
#     electron = _Electron
#
#     class _Electron(_PelpiObject):
#
#         hot = _Hot
#
#         class _Hot(_PelpiObject):
#
#             def temperature(self):
#                 """
#                 Return an estimate of the hot electron temperature from the Haines2009 model.
#
#                 .. math:
#                     T_e^h = (\sqrt{1 + \sqrt{2} \ a_0} - 1 ) m_e c^2
#                     with $T_e^h$ the hot electron temperature
#                     $a_0$ the normalized laser intensity
#                     $m_e c^2$ the electron mass energy
#                 """
#                 a0 = _lpi.laser.intensity_peak_normalized()
#                 return ((1.0 + 2.0**(1/2.) * a0)**(1/2.) - 1.0) * 511 * _u('keV')

class Haines2009(_PelpiObject):
    """
    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi       = LaserPlasmaInteraction

    def electron_hot_temperature(self):
        """
        Return an estimate of the hot electron temperature from the Haines2009 model.

        .. math:
            T_e^h = (\sqrt{1 + \sqrt{2} \ a_0} - 1 ) m_e c^2
            with $T_e^h$ the hot electron temperature
            $a_0$ the normalized laser intensity
            $m_e c^2$ the electron mass energy
        """
        a0 = self._lpi.laser.intensity_peak_normalized()
        return ((1.0 + 2.0**(1/2.) * a0)**(1/2.) - 1.0) * 511 * _u('keV')

class Wilks1992(_PelpiObject):
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
        self._lpi       = LaserPlasmaInteraction

    def electron_hot_temperature(self):
        """
        Return an estimate of the hot electron temperature from the Wilks1992 model.

        .. math:
            T_e^h = (\sqrt{1 + a_0^2} - 1 ) m_e c^2
            with $T_e^h$ the hot electron temperature
            $a_0$ the normalized laser intensity
            $m_e c^2$ the electron mass energy
        """
        a0 = self._lpi.laser.intensity_peak_normalized()
        return ((1.0 + (a0)**2)**(1/2.) - 1.0 ) * 511 * _u('keV') # TODO: a0 or a0/2 ?


################################################################################
class Common(_PelpiObject):
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
        self._lpi       = LaserPlasmaInteraction

    def target_conductivity(self,temperature_cold,log_coulomb):
        """
        Spitzer conductivity.

        .. math :
            \\frac{(4 \pi \epsilon_0)^2 (k_b T_e^{cold})^{3/2}}{\pi Z e^2 \sqrt{m_e} \ln(\Lambda)}
        """
        Tec = temperature_cold
        lnC = log_coulomb
        return (4*_np.pi*_u.epsilon_0)**2 * (Tec*_u.m_e*_u.c**2)**(3/2.) / (_np.pi*self._lpi.target.mat.Z * _u.e**2 * _u.m_e**(1/2.) * lnC)

    def laser_efficiency_absorption(self):
        return _u.Quantity(0.5)

    def electron_distribution(self,distribution,kinetic_energy,temperature):
        """

        """
        available=["MB"]
        Ek = kinetic_energy
        Te = temperature

        if distribution=="MB":
            return _np.sqrt(4/_np.pi) * _np.sqrt(Ek/Te**3) * _np.exp( -Ek/Te )
        # elif distribution=="MJ":
        #     """
        #     From A. Aliano, L. Rondoni, G.P. Morriss,
        #     Maxwell-Juttner distributions in relativistic molecular dynamics, 2005
        #     (2D)
        #     """
        #     Ek=kinetic_energy
        #     Te=temperature
        #
        #     Em=1 * _u.m_e * _u.c**2
        #     a=Em/Te
        #     d=(1/(2 * _np.pi * _u.m_e**2 * _u.c**2)) * (a**2 * _np.exp(a))/(1 + a)
        #
        #     return (2* _np.pi/_u.c**2) * d * (Ek + Em) * _np.exp(-a * (Ek + Em)/Em)
        # elif distribution=="MJ":
        #     """
        #     From Wright 1975, in the rest frame
        #     """
        #     Em=1 * _u.m_e * _u.c**2
        #
        #     gammaR=(kinetic_energy/Em + 1 )
        #     xiR=Em/temperature
        #     # nR = self._lpi.target.material.electronNumberDensity()
        #     nR = 1
        #
        #     from scipy.special import kn
        #
        #     return (nR * xiR)/(4 * _np.pi * kn(2,xiR)) * _np.exp(- xiR*gammaR)
        elif distribution=="MJ":
            """
            From Wright 1975, in the rest frame
            """
            Em =1 * _u.m_e * _u.c**2
            Ek = kinetic_energy
            Te = temperature

            # nR = self._lpi.target.material.electronNumberDensity()
            nR = 1
            from scipy.special import kn

            return (nR)/(4 * _np.pi * Te * kn(2,Em/Te)) * _np.exp(- (Ek + Em)/Te)
        else:
            if type(distribution)!=str:
                raise TypeError("'distribution' type must be 'string', but it is "+str(type(distribution)))

            raise NameError("Distribution name "+distribution+" not found. Available are "+str(available))


    def electron_number_total(self,temperature,absorption_efficiency):
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
        Te = temperature

        ne = self._lpi.laser.energy()/(3/2. * Te)
        return ne.to(_du['number'])
