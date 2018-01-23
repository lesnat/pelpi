#coding:utf8
from ._global import *
from ._tools import _PelpiObject

__all__ = ["Profile","Laser"]

class Profile(_PelpiObject):
    """
    Class for defining spatial and temporal pulse profiles.

    Yet only simple profiles are accepted (depends only on radius).

    Parameters
    ---------
    time_profile : str
        Temporal profile of the pulse. Available : ``gaussian``
    space_profile : str
        Spatial profile of the pulse (waist). Available : ``gaussian``, ``top-hat``

    time_fwhm : time quantity, optional
        Temporal Full Width Half Maximum of the laser pulse.
    space_fwhm : length quantity, optional
        Spatial Full Width Half Maximum of the laser pulse.
    space_radius : length quantity, optional
        Spatial radius of the laser pulse.

    Notes
    -----
    If ``time_profile`` is ``gaussian``, you must define ``time_fwhm``.

    If ``space_profile`` is ``gaussian``, you must define ``space_fwhm``.

    If ``space_profile`` is ``top-hat``, you must define ``space_radius``.


    Examples
    --------
    You can set a laser profile as follows :

    >>> import pelpi as pp
    >>> prof = pp.Profile(
    ...    time_profile  = "gaussian",
    ...    time_fwhm     = 30 * pp.unit('fs'),
    ...    space_profile = "top-hat",
    ...    space_radius  = 10 * pp.unit('um')
    ...    )
    ...
    """
    def __init__(self,time_profile,space_profile,\
                time_fwhm=None,\
                space_fwhm=None,space_radius=None):
        self._time_profile   = time_profile
        self._time_fwhm      = time_fwhm
        self._space_profile  = space_profile
        self._space_fwhm     = space_fwhm
        self._space_radius   = space_radius

        self._checkInput(variable_dictionnary={\
            'time_profile':str,'space_profile':str,\
            'time_fwhm':type(_u('s')),
            'space_fwhm':type(_u('m')),'space_radius':type(_u('m')),\
            }) # TODO: How to do this with NoneType object ?

    def time_profile(self):
        """
        """
        return self._time_profile

    def time_fwhm(self):
        """
        """
        return self._time_fwhm

    def space_profile(self):
        """
        """
        return self._space_profile

    def space_fwhm(self):
        """
        """
        return self._space_fwhm

    def space_radius(self):
        """
        """
        return self._space_radius

    def timeEnvelope(self,t):
        """
        Returns
        -------
        Time pulse envelope at given time : dimensionless quantity

        Parameters
        ----------
        t : time quantity
            Time.

        Notes
        -----
        timeEnvelope is centered at t=0, and has a maximum value of 1.
        """
        if self.time_profile()=="gaussian":
            t0=self.time_fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(t/t0)**2)

    def spaceEnvelope(self,r):
        """
        Returns
        -------
        Space pulse envelope at given radius : dimensionless quantity

        Parameters
        ----------
        r : length quantity
            Radius.

        Notes
        -----
        spaceEnvelope is centered at r=0 and has a maximum value of 1.
        """
        if self.space_profile()=="gaussian":
            r0=self.space_fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(r/r0)**2)
        elif self.space_profile()=="supergaussian":
            n=10
            return _np.exp(-(2*_np.sqrt(_np.log(2))*r/self.space_fwhm())**(2*n))
        elif self.space_profile()=="top-hat":
            if abs(r)<self.space_radius():
                return 1.0
            else:
                return 0.0

    def envelope(self,r,t):
        """
        Returns
        -------
        Pulse envelope at given time and radius : dimensionless quantity

        Parameters
        ----------
        r : length quantity
            Radius.
        t : time quantity
            Time.

        Notes
        -----
        envelope is centered at t=0 and r=0, and has a maximum value of 1.
        """
        return self.spaceEnvelope(r) * self.timeEnvelope(t)

    def timeIntegral(self,lower_edge=None,upper_edge=None,number_points=None):
        """
        Returns
        -------
        Integration of timeEnvelope under time : time quantity

        Parameters
        ----------
        lower_edge : float, optional
            Lower edge of integration
        upper_edge : float, optional
            Upper edge of integration
        number_points : int, optional
            Number of points to use

        Notes
        -----
        Some analytical solutions exists for time profiles :

        ``gaussian`` :

        .. math:: S_0^t = \sqrt{\pi} \\frac{t_{FWHM}}{2 \sqrt{\ln{2}}}

        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.time_profile()=="gaussian":
            t0=self.time_fwhm()/(2 * _np.sqrt(_np.log(2)))
            S0t=t0 * _np.sqrt(_np.pi)
            return S0t
        else:
            raise NameError("Unknown laser time profile name.")

    def spaceIntegralDouble(self,lower_edge=None,upper_edge=None,number_points=None):
        """
        Returns
        -------
        Double integration of the space envelope under radius: length**2 quantity

        Parameters
        ----------
        lower_edge : float, optional
            Lower edge of integration
        upper_edge : float, optional
            Upper edge of integration
        number_points : int, optional
            Number of points to use

        Notes
        -----
        Some analytical solutions exists for space profiles :

        ``gaussian`` :

        .. math:: S_r^0 = \pi (\\frac{r_{FWHM}}{2 \sqrt{\ln{2}}})^2

        ``top-hat`` :

        .. math:: S_r^0 = \pi r^2


        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.space_profile()=="gaussian":
            r0=self.space_fwhm()/(2 * _np.sqrt(_np.log(2)))
            S0r=_np.pi * r0**2
            return S0r
        elif self.space_profile()=="top-hat":
            return _np.pi*self.space_radius()**2
        else:
            raise NameError("Unknown laser space profile name.")



class Laser(_PelpiObject):
    """
    Class for defining laser characteristics, and do some simple calculations.

    Parameters
    ----------
    wavelength : length quantity
        Laser monochromatic wavelength
    energy : energy quantity
        Total energy of the laser pulse
    profile : object
        Instanciated ``Profile`` object

    Examples
    --------
    Assuming you defined a ``Profile`` object as ``prof``, you can instanciate a ``Laser`` class as follows

    >>> laser=pp.Laser(
    ...    wavelength = 0.8 * pp.unit('um'),
    ...    energy     = 2.0 * pp.unit('J'),
    ...    Profile    = prof
    ...    )
    ...

    and then print some calculations

    >>> print("Laser peak intensity : {}".format(laser.intensity(r=0*pp.unit('m'),t=0*pp.unit('s'))))
    >>> print("Laser normalized intensity : {}".format(laser.intensityNormalized()))
    >>> print("Critical number density : {}".format(laser.numberDensityCritical()))
    """
    def __init__(self,wavelength,energy,Profile,**kwargs):
        self._wavelength = wavelength
        self._energy     = energy

        self.profile    = Profile

        self._checkInput(variable_dictionnary={})

    def wavelength(self):
        """
        """
        return self._wavelength

    def energy(self):
        """
        """
        return self._energy

    def pulsation(self):
        return 2*_np.pi*_u.c/self.wavelength()

    def numberDensityCritical(self):
        """
        Return the critical number density.
        """
        return _u.m_e*_u.epsilon_0*(self.pulsation()/_u.e)**2

    def power(self,r=0*_u('m'),t=0*_u('s')):
        return self.energy()/self.profile.timeIntegral() * self.profile.envelope(r,t)

    def intensity(self,r=0*_u('m'),t=0*_u('s')):
        return self.power(r,t)/self.profile.spaceIntegralDouble()

    def intensityPeakNormalized(self):
        """
        Returns
        -------
        Normalized laser peak intensity : dimensionless quantity

        Notes
        -----
        The normalized laser intensity :math:`a_0` is defined as follows :

        .. math:: a_0 = 0.85 \\times \sqrt{I_{18} \lambda_{\mu}^2}

        with :math:`I_{18}` the laser peak intensity in :math:`10^{18} W.cm^{-2}`
        and :math:`\lambda_{\mu}` the laser wavelength in :math:`10^{-6} m`.
        """
        return 0.85*_np.sqrt(\
                (self.intensity(r=0*_u('m'),t=0*_u('s')).to('W/cm**2')*(self.wavelength().to('um'))**2)\
                /(1.e18 * _u('W*um**2/cm**2')))

    def timeChirp(self,t,phase=0.0 *_u('deg')):
        return _np.sin(self.pulsation().to(t.units**-1) * t - phase)
