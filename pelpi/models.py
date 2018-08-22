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
    Short Description : This is an example model, for developers.
    
    Hypotheses
    ----------
    List of hypotheses or numerical/experimental parameters used in the paper
    Code
        2D PIC code
        ...
        
    Target
        Solid aluminium
        ...
        
    Laser
        Intensity :math:`I = 10^{18} W.cm^{-2}`
        ...

    Reference
    ---------
    Authors
    Title
    Journal, year

    Notes
    -----
    Additional informations : Just copy-paste this example class and adapt it.

    Please write a short doc like this and update the LaserPlasmaInteraction call method.
    It would also be great to write a short test to ensure that the results of the method
    will not be broken during further developments.
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

            # Do not initialize dict, same reason as previously

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
                Returns
                -------
                Here write what does return the method
                
                Notes
                -----
                This is an example note to explain how the calculation is done
                
                .. math: n = \\frac{n_e}{n_c}
                
                with :math:`n` the normalized electron density
                :math:`n_e` the electron number density
                :math:`n_c` the laser critical density
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
                param initialization ...
                """
                pass

        class _Cold(_PelpiObject):
            def __init__(self,lpi):
                self._lpi   = lpi

    class _Ion(_PelpiObject):
        def __init__(self,lpi):
            self._lpi=lpi

    class _Positron(_PelpiObject):
        def __init__(self,lpi):
            self._lpi=lpi

    class _Photon(_PelpiObject):
        def __init__(self,lpi):
            self._lpi=lpi


################################################################################
class Beg1997(_PelpiObject):
    """
    Experimental study of ultra-intense laser solid interaction
    
    Hypotheses
    ----------    
    Target
      Material from CH to Cu
      Few 10 micrometers thick

    Laser
      Wavelength 1.053 micrometer
      Pulse duration 0.7 to 1.3 ps
      Intensity between :math:`10^{17}` and :math:`10^{19} W.cm^{-2}`
      Contrast :math:`1:10^{-6}`
      p polarized
      Incidence 30 degrees 
      Spot size about 12 micrometers
    
    Reference
    ---------
    F. N. Beg, A. R. Bell, A. E. Dangor, C. N. Danson, A. P. Fews, M. E. Glinsky,B. A. Hammel, P. Lee, P. A. Norreys, and M. Tatarakis
    A study of picosecond laser–solid interactions up to :math:`10^{19} W.cm^{-2}`
    Physics of Plasmas, 1997
    
    Notes
    -----
    Predominant absorption mechanism seems to be resonance absorption
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
                Returns
                -------
                Hot electron temperature
                
                Notes
                -----
                
                .. math: T_e^h = 100 * (\\frac{I_{17} \lambda_{\mu}^2})^(1/3)
                    
                with :math:`T_e^h` the hot electron temperature in keV
                :math:`I_{17}` the laser peak intensity in :math:`10^{17} W.cm^{-2}`
                :math:`\lambda_{\mu}` the laser wavelength in micrometer
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
            Returns
            -------
            Maximum ion energy
            
            Notes
            -----
            
            .. math: E_{max} = 1.2 \pm (0.3) \\times 10^{-2} (I/W.cm^{-2})^{0.313 \pm 0.03} keV
            """
            return (1.2e-2*_u('keV')) * (self._lpi.laser.I0.to('W/cm**2'))**(0.313)

class Haines2009(_PelpiObject):
    """
    Theoretical model on ...
    
    Hypotheses
    ----------
    
    
    
    
    Reference
    ---------
    M. G. Haines,1,2 M. S. Wei, F. N. Beg, and R. B. Stephens
    Hot-Electron Temperature and Laser-Light Absorption in Fast Ignition
    Physical Review Letters, 2009
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
                Returns
                -------
                Hot electron temperature

                Notes
                -----
                
                .. math: T_e^h = (\sqrt{1 + \sqrt{2} \ a_0} - 1 ) m_e c^2

                with :math:`T_e^h` the hot electron temperature
                :math:`a_0` the normalized laser intensity
                :math:`m_e c^2` the electron mass energy
                """
                a0 = self._lpi.laser.intensity_peak_normalized()
                return ((1.0 + 2.0**(1/2.) * a0)**(1/2.) - 1.0) * 511 * _u('keV')






