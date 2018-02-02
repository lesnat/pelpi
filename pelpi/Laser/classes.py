#coding:utf8
from .._global import *
from .._tools import _PelpiObject

__all__ = ["Laser"]

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
    def __init__(self,wavelength,energy,time_profile,space_profile,**kwargs):
        self._wavelength = wavelength
        self._energy     = energy

        self.time_profile  = time_profile
        self.space_profile  = space_profile

        self.electron   = _Electron(self)

        # self._checkInput(variable_dictionnary={})

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
        return self.space_profile.envelope(r) * self.time_profile.envelope(t)

    def power(self,r=0*_u('m'),t=0*_u('s')):
        return self.energy()/self.time_profile.integral1D() * self.envelope(r,t)

    def intensity(self,r=0*_u('m'),t=0*_u('s')):
        return self.power(r,t)/self.space_profile.integral2D()

    def intensity_peak_normalized(self):
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

    def time_chirp(self,t,phase=0.0 *_u('deg')):
        return _np.sin(self.pulsation().to(t.units**-1) * t - phase)

class _Electron(_PelpiObject):
    def __init__(self,Laser):
        self._las = Laser

    def number_density_critical(self):
        """
        Return the critical number density.
        """
        return _u.m_e*_u.epsilon_0*(self._las.pulsation()/_u.e)**2
