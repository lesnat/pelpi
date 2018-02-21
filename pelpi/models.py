#coding:utf8
from ._global import *
from ._tools import _PelpiObject
################################################################################
"""
Model doc.

Of course no default behaviour for model estimates

Malka 2001 -> Scaling Energie max electrons
"""
################################################################################
class _ExampleModel(_PelpiObject):
    """
    This is an example model, for developers.

    Just copy-paste this example and adapt it.

    Then, please check in the LaserPlasmaInteraction object if a method name with the same 'path' as the model method exists
    If yes, just update the doc of the correspondant lpi method,
    otherwise, create a new method in lpi.
    """
    def __init__(self,lpi):
        # Test user input
        self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")

        # Do not initialize default dict because models should always return an estimate and not a default behaviour

        # A reference to the lpi instance can be saved in private attribute,
        # but it is not necessary untill methods are defined in sub-objects

        # Instanciate sub-classes (with the same structure as in lpi)
        self.electron   = self._Electron(lpi)
        self.ion        = self._Ion(lpi)
        self.photon     = self._Photon(lpi)
        self.positron   = self._Positron(lpi)


    class _Electron(_PelpiObject):
        def __init__(self,lpi):
            # Do not test input because it was already tested.

            # Do not initialize dict, same reason

            # Save reference to the lpi instance or not, depending on the case
            self._lpi   = lpi

            # Instanciate sub-classes
            self.hot    = self._Hot(lpi)
            self.cold   = self._Cold(lpi)

        class _Hot(_PelpiObject):
            def __init__(self,lpi):
                # Save reference to the lpi instance
                self._lpi   = lpi

            def example_method(self):
                """
                Documentation
                """
                # Save some intermediate values
                ne = self._lpi.target.material.electron.number_density()
                nc = self._lpi.laser.electron.number_density_critical()

                # Do the calculus
                ne_over_nc = ne/nc

                # Return the result, converted to the appropriate unit (_du = pelpi.default_unit)
                return ne_over_nc.to(_du['number'])

            def example_method_with_param(self,param1=None,param2=None):
                """
                Always initialize param to None ; this way ...
                """
                pass

        class _Cold(_PelpiObject):
            def __init__(self,lpi):
                self._lpi   = lpi

    class _Ion(_PelpiObject):
        def __init__(self,lpi):
            pass

    class _Positron(_PelpiObject):
        def __init__(self,lpi):
            pass

    class _Photon(_PelpiObject):
        def __init__(self,lpi):
            pass


################################################################################
class Beg1997(_PelpiObject):
    """
    Class for estimating ...
    Experimental fit

    hypotheses

    reference
    ...
    Experimental laser intensity etc ...
    """
    def __init__(self,lpi):
        self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")
        self.electron=self._Electron(lpi)
        self.ion=self._Ion(lpi)

    class _Electron(_PelpiObject):
        def __init__(self,lpi):
            self.hot = self._Hot(lpi)

        class _Hot(_PelpiObject):
            def __init__(self,lpi):
                self._lpi=lpi

            def temperature(self):
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

    class _Ion(_PelpiObject):
        def __init__(self,lpi):
            self._lpi = lpi

        def energy_cutoff(self):
            """
            Return the maximum ion energy
            """
            return (1.2e-2*_u('keV')) * (self._lpi.laser.I0.to('W/cm**2'))**(0.313)

class Haines2009(_PelpiObject):
    """
    """
    def __init__(self,lpi):
        self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")
        self.electron=self._Electron(lpi)

    class _Electron(_PelpiObject):
        def __init__(self,lpi):
            self.hot = self._Hot(lpi)

        class _Hot(_PelpiObject):
            def __init__(self,lpi):
                self._lpi=lpi


            def temperature(self):
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



class Price1995(_PelpiObject):
    pass

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

    def __init__(self,lpi):
        self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")
        self.electron=self._Electron(lpi)

    class _Electron(_PelpiObject):
        def __init__(self,lpi):
            self.hot = self._Hot(lpi)

        class _Hot(_PelpiObject):
            def __init__(self,lpi):
                self._lpi=lpi

            def temperature(self):
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
        eta_l = absorption_efficiency

        ne = eta_l * self._lpi.laser.energy()/(3/2. * Te)
        return ne.to(_du['number'])
