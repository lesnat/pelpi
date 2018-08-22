#coding:utf8

from ._global import *
from ._tools import _PelpiObject,_Default,_estimate
from .plasma import _PlasmaParameters

__all__ = ["LaserPlasmaInteraction"]

################################################################################
class LaserPlasmaInteraction(_PelpiObject):
    """
    Class for estimations in laser-plasma interaction.

    Parameters
    ----------
    laser : object
        pelpi ``Laser`` instance
    target : object
        pelpi ``Target`` instance

    Attributes
    ----------
    laser : object
        Input laser instance
    target : object
        Input target instance
    electron : object
        Contains estimations about electrons
    plasma : object
        Contains usual plasma parameters

    Notes
    -----
    Even if the code structure permit not to give a lot of parameters
    to perform an estimate, some complex models may need several of them to give the result.

    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.

    To do this, pelpi needs the parameters to be defined explicitly, i.e. with the parameter
    name in the method call.

    See examples.

    Examples
    --------
    Here is a quick example, assuming ``lpi`` is an instance of ``LaserPlasmaInteraction``

    >>> eh = lpi.electron.hot
    >>> # Define the laser absorption efficiency
    >>> eta_l = 0.1 * pp.unit('')
    >>> # Use a simple model to get a temperature estimate
    >>> Teh = eh.temperature(model='Haines2009')
    >>> # The model needs a temperature & absorption efficiency to return a result
    >>> neh = eh.number_total(model="Common",temperature = Teh, absorption_efficiency = eta_l) # This works
    ...
    >>> neh = eh.number_total(model="Common", Teh, eta_l) # This does not work

    """
    def __init__(self,laser,target):
        # Test user input
        self._check_input('laser',laser,"<class 'pelpi.laser.Laser'>")
        self._check_input('target',target,"<class 'pelpi.target.Target'>")

        # Do not initialize default dict because there is no direct access to a method from this point

        # Save references to target & laser instances into attributes
        self.laser      = laser
        self.target     = target

        # Instanciate sub-classes
        self.plasma     = _PlasmaParameters(self)
        self.electron   = _LPIElectron(self)
        # self.ion        = Ion(self)


class _LPIElectron(_PelpiObject):
    """
    Electrons properties.

    Attributes
    ----------
    hot : object
        Containing properties of super-thermal electrons, in Ultra-High Intensity regime
    """
    def __init__(self,LaserPlasmaInteraction):
        # No need to check input because this method is only called in LaserPlasmaInteraction definition

        # Save reference to LaserPlasmaInteraction instance in a private variable
        self._lpi   = LaserPlasmaInteraction

        # Add shortcuts to methods previously defined about electrons
        # WARNING ! Change default here would not affect the program ? Or change ne/nc access to this point
        self.number_density = self._lpi.target.material.electron.number_density
        self.number_density_critical = self._lpi.laser.electron.number_density_critical

        # Initialize default dict after the shortcuts have been defined
        self.default = _Default(self)

        # Instanciate sub-classes
        self.hot    = _LPIElectronHot(self._lpi)
        # self.cold   = self._Cold(self._lpi)

    def efficiency_absorption(self,model,**kargs):
        """
        Return an estimate of the laser absorption efficiency into electrons.

        Arguments
        --------
        model : string
            Model name
        **kargs
            Model input parameters

        References
        ----------
        Price1995
          Type :
            experimental
          kargs :
            None
          Equation :
            :math:`\eta_l = 0.1`
            with :math:`\eta_l` electron absorption efficiency
          Reference :
            D. F. Price, R. M. More, R. S. Walling, G. Guethlein, R. L. Shepherd, R. E. Stewart, and W. E. White
            Absorption of Ultrashort Laser Pulses by Solid Targets Heated Rapidly to Temperatures 1—1000 ev
            Physical Review Letters, 1995
        """
        dim = 'number'

        if model == "Price1995":
          eta_l = 0.1
        else:
          raise NameError('Unknown model name')

        return self.default.result('efficiency_absorption',eta_l,dim)

    def number_total(self,model,**kargs):
        """
        Return an estimate of the total electron number.

        Arguments
        --------
        model : string
            Model name
        **kargs
            Model input parameters

        References
        ----------
        Common
          Type :
            theoretical
          kargs :
            `temperature`, electron temperature.
            `efficiency_absorption`, laser absorption efficiency into electrons.
          Equation :
            :math:`n_0 = \\frac{\eta_{l} E_{l}}{3/2 T_e^{hot}}`
            with :math:`n_0` the hot electron total number,
            :math:`\eta_l` the laser absorption efficiency into hot electrons,
            :math:`E_l` the laser total energy,
            :math:`T_e^{hot}` the thermal energy of hot electrons.
          Reference :
            Based on Maxwell-Boltzmann law
        """
        dim = 'number'

        if model == "Common":
          Te = kargs['temperature']
          eta_l = kargs['efficiency_absorption']
          ne = eta_l * self._lpi.laser.energy()/(3/2. * Te)
        else:
          raise NameError("Unknown model name")

        return self.default.result('number_total',ne,dim)


class _LPIElectronHot(_PelpiObject):
    """
    Super-thermal electrons, in Ultra-High Intensity regime.
    """
    def __init__(self,LaserPlasmaInteraction):
        # No need to check input because this method is only called in LaserPlasmaInteraction definition

        # Initialise default dict
        self.default = _Default(self)

        # Save reference to LaserPlasmaInteraction instance in a private variable
        self._lpi   = LaserPlasmaInteraction

    def temperature(self,model,**kargs):
        """
        Returns
        -------
        Estimate of the hot electron temperature.

        Arguments
        --------
        model : string
            Model name
        **kargs
            Model input parameters

        References
        ----------
        Beg1997
          Type :
            empirical
          kargs :
            None
          Equation :
            :math:`T_e^h = 100 * (\\frac{I_{17} \lambda_{\mu}^2})^(1/3)`
            with :math:`T_e^h` the hot electron temperature in keV
            :math:`I_{17}` the laser peak intensity in :math:`10^{17} W.cm^{-2}`
            :math:`\lambda_{\mu}` the laser wavelength in micrometer
          Reference :
            F. N. Beg, A. R. Bell, A. E. Dangor, C. N. Danson, A. P. Fews, M. E. Glinsky,B. A. Hammel, P. Lee, P. A. Norreys, and M. Tatarakis
            A study of picosecond laser–solid interactions up to :math:`10^{19} W.cm^{-2}`
            Physics of Plasmas, 1997

        Haines2009
          Type :
            theoretical
          kargs :
            None
          Equation :
            :math:`T_e^h = (\sqrt{1 + \sqrt{2} \ a_0} - 1 ) m_e c^2`
            with :math:`T_e^h` the hot electron temperature
            :math:`a_0` the normalized laser intensity
            :math:`m_e c^2` the electron mass energy
          Reference :
            M. G. Haines,1,2 M. S. Wei, F. N. Beg, and R. B. Stephens
            Hot-Electron Temperature and Laser-Light Absorption in Fast Ignition
            Physical Review Letters, 2009

        Wilks1992
          Type :
            numerical
          kargs :
            None
          Equation :
            :math:`T_e^h = (\sqrt{1 + a_0^2} - 1 ) m_e c^2`
            with :math:`T_e^h` the hot electron temperature
            :math:`a_0` the normalized laser intensity
            :math:`m_e c^2` the electron mass energy
          Reference :
            S. C. Wilks, W. L. Kruer, M. Tabak, and A. B. Langdon
            Absorption of Ultra-Intense Laser Pulses
            Physical Review Letters, 1992
        """
        dim = 'temperature'

        if model == "Wilks1992":
          a0 = self._lpi.laser.intensity_peak_normalized()
          Teh = ((1.0 + (a0)**2)**(1/2.) - 1.0 ) * _u.m_e * _u.c**2 # TODO: a0 or a0/2 ?
        elif model == "Haines2009":
          a0 = self._lpi.laser.intensity_peak_normalized()
          Teh = ((1.0 + 2.0**(1/2.) * a0)**(1/2.) - 1.0) * _u.m_e * _u.c**2
        elif model == "Beg1997":
          I0 = self._lpi.laser.intensity()
          lambda_laser = self._lpi.laser.wavelength()
          Teh = 100.*_u('keV') * ((I0 * lambda_laser**2) / (1e17*_u('W/cm**2')*_u('um**2')) )**(1/3.)
        else:
          raise NameError("Unknown model name")

        return self.default.result('temperature',Teh,dim)


class _LPIIon(_PelpiObject):
    """
    Ion properties.
    """
    def __init__(self,LaserPlasmaInteraction):
      # No need to check input because this method is only called in LaserPlasmaInteraction definition

      # Save reference to LaserPlasmaInteraction instance in a private variable
      self._lpi   = LaserPlasmaInteraction

      # Initialize default dict after the shortcuts have been defined
      self.default = _Default(self)

    def energy_cutoff(self,model,**kargs):
        """
        Returns
        -------
        Estimate of the ion energy cutoff.

        Arguments
        --------
        model : string
            Model name
        **kargs
            Model input parameters

        References
        ----------
        Beg1997
          Type :
            empirical
          kargs :
            None
          Equation :
            :math:`E_{max} = 1.2 \pm (0.3) \\times 10^{-2} (I/W.cm^{-2})^{0.313 \pm 0.03} keV`
          Reference :
            F. N. Beg, A. R. Bell, A. E. Dangor, C. N. Danson, A. P. Fews, M. E. Glinsky,B. A. Hammel, P. Lee, P. A. Norreys, and M. Tatarakis
            A study of picosecond laser–solid interactions up to :math:`10^{19} W.cm^{-2}`
            Physics of Plasmas, 1997
        """
        dim = 'energy'

        if model == "Beg1997":
          I0 = self._lpi.laser.intensity()
          Emax = 1.2e-2 * _u('keV') * (I0/_u('W/cm**2'))**(0.313)
        else:
          raise NameError("Unknown model name")

        return self.default.result('energy_cutoff',Emax,dim)
