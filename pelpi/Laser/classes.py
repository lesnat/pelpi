#coding:utf8
from .._global import *
from .._tools import _PelpiObject

__all__ = ["Laser"]

class Laser(_PelpiObject):
    """
    Class for defining laser characteristics, and do some simple calculations.

    Parameters
    ----------
    time_profile : object
        Pulse time profile. pelpi ``Profile`` instance
    space_profile : object
        Pulse space profile (waist). pelpi ``Profile`` instance
    wavelength : length Quantity
        Laser monochromatic wavelength
    energy : energy Quantity
        Total energy of the laser pulse
        
    Attributes
    ----------
    time_profile : object
        Input time_profile object
    space_profile : object
        Input space_profile object

    Examples
    --------
    Assuming you defined two ``Profile`` objects as ``tprof`` and ``sprof``, you can instanciate a ``Laser`` class as follows

    >>> laser=pp.Laser(
    ...    wavelength       = 0.8 * pp.unit('um'),
    ...    energy           = 2.0 * pp.unit('J'),
    ...    time_profile     = tprof,
    ...    space_profile    = sprof
    ...    )
    ...

    and then print some calculations

    >>> I0 = laser.intensity(r=0*pp.unit('um'),t=0*pp.unit('fs'))
    >>> print("Laser peak intensity : {}".format(I0))
    >>> a0 = laser.intensity_peak_normalized()
    >>> print("Laser normalized peak intensity : {}".format(a0))
    >>> nc = laser.electron.number_density_critical()
    >>> print("Critical number density : {}".format(nc))
    """
    def __init__(self,time_profile=None,space_profile=None,wavelength=None,energy=None):
        # Test user input
        self._check_input('time_profile'    ,time_profile   ,"<class 'pelpi.Profile.classes.Profile'>")
        self._check_input('space_profile'   ,space_profile  ,"<class 'pelpi.Profile.classes.Profile'>")
        self._check_input('wavelength'      ,wavelength     , type(_du['length']))
        self._check_input('energy'          ,energy         , type(_du['energy']))
        
        # Initialize default dict
        self._initialize_defaults(input_dict={'wavelength':wavelength,'energy':energy})

        # Save references to Profile instances
        self.time_profile  = time_profile # TODO: save as attr or in default or both ?
        self.space_profile  = space_profile

        # Instanciate sub-class
        self.electron   = self._Electron(self)

    def wavelength(self):
        """
        Returns
        -------
        User input `wavelength` : length Quantity
        """
        return self.default['wavelength']

    def energy(self):
        """
        Returns
        -------
        User input `energy` : energy Quantity
        """
        return self.default['energy']

    def pulsation(self):
        """
        Returns
        -------
        Laser pulsation : 1/time Quantity
        
        Notes
        -----
        pulsation is defined as follows
        
        .. math: \omega_l = \\frac{2 \pi c}{\lambda}
        """
        wl = (2*_np.pi*_u.c/self.wavelength())
        return wl.to(_du['pulsation'])

    def envelope(self,r,t):
        """
        Returns
        -------
        Pulse envelope at given time and radius : dimensionless Quantity

        Parameters
        ----------
        r : length Quantity
            Radius
        t : time Quantity
            Time

        Notes
        -----
        envelope is centered at t=0 and r=0, and has a maximum value of 1.
        """
        env = self.space_profile.envelope(r) * self.time_profile.envelope(t)
        return env.to('')

    def power(self,r=0*_u('m'),t=0*_u('s')):
        """
        Returns
        -------
        Power at given time and radius : power Quantity
        
        Parameters
        ----------
        r : length Quantity
            Radius
        t : time Quantity
            Time
        
        Notes
        -----
        Default behaviour gives the peak power.
        
        power is defined as follows
        
        .. math: P(r,t) = \\frac{E_l}{S_0^t} profile(r,t)
        """
        P = self.energy()/self.time_profile.integral1D() * self.envelope(r,t)
        return P.to(_du['power'])

    def intensity(self,r=0*_u('m'),t=0*_u('s')):
        """
        Returns
        -------
        Intensity at given time and radius : power/length**2 Quantity
        
        Parameters
        ----------
        r : length Quantity
            Radius
        t : time Quantity
            Time
        
        Notes
        -----
        Default behaviour gives the peak intensity.
        
        Intensity is defined as follows
        
        .. math: I(r,t) = \\frac{P(r,t)}{S_0^r}
        """
        I = self.power(r,t)/self.space_profile.integral2D()
        return I.to(_du['intensity'])

    def intensity_peak_normalized(self): # TODO: calculate with the original definition
        """
        Returns
        -------
        Normalized laser peak intensity : dimensionless Quantity

        Notes
        -----
        The normalized laser intensity :math:`a_0` is defined as follows

        .. math:: a_0 = 0.85 \\times \sqrt{I_{18} \lambda_{\mu}^2}

        with :math:`I_{18}` the laser peak intensity in :math:`10^{18} W.cm^{-2}`
        and :math:`\lambda_{\mu}` the laser wavelength in :math:`10^{-6} m`.
        """
        I0 = self.intensity(r=0*_u('m'),t=0*_u('s'))
        a0 = 0.85*_np.sqrt((I0*(self.wavelength())**2)/(1.e18*_u('W*um**2/cm**2')))
        return a0.to(_du['number'])

    class _Electron(_PelpiObject):
        """
        Electron properties.
        """
        def __init__(self,Laser):
            # No need to check input because this method is only called in Laser definition.
            
            # Initialise default dict
            self._initialize_defaults()
            
            # Save reference to Laser instance in a private variable
            self._las = Laser

        def number_density_critical(self):
            """
            Returns
            -------
            Electron critical number density : 1/length**3 Quantity
            
            Notes
            -----
            Electron critical number density is defined as follows
            
            .. math: TODO
            """
            nc = _u.m_e*_u.epsilon_0*(self._las.pulsation()/_u.e)**2
            return nc.to(_du['number_density'])
        
