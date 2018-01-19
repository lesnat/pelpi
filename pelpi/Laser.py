#coding:utf8
import numpy as _np
from . import unit as _u
from . import prefered_unit as _pu


__all__ = ["Profile","Laser"]

class Profile(object):
    """
    class for defining pulse profile envelope

    Parameters
    ---------
    time_profile, string
        Temporal profile of the pulse
        Available profiles :
            "gaussian",
            You must define the time_fwhm variable for setting the time full width half maximum

    space_profile, string
        Spatial profile of the pulse (waist).
        Available profiles :
            "gaussian",
            You must define the space_fwhm variable for setting the spatial full width half maximum (waist)

            "top-hat",
            You must define the space_radius variable for setting the spatial radius (waist)

    """
    def __init__(self,time_profile,space_profile,**kwargs):
        self.time_profile   = time_profile
        self.time_fwhm      = kwargs.get('time_fwhm',None)
        self.space_profile  = space_profile
        self.space_fwhm     = kwargs.get('space_fwhm',None)
        self.space_radius   = kwargs.get('space_radius',None)

    def timeEnvelope(self,t):
        if self.time_profile=="gaussian":
            t0=self.time_fwhm/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(t/t0)**2)

    def spaceEnvelope(self,r):
        if self.space_profile=="gaussian":
            r0=self.space_fwhm/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(r/r0)**2)
        elif self.space_profile=="supergaussian":
            n=10
            return _np.exp(-(2*_np.sqrt(_np.log(2))*r/self.space_fwhm)**(2*n))
        elif self.space_profile=="top-hat":
            if abs(r)<self.space_radius:
                return 1.0
            else:
                return 0.0

    def timeIntegral(self):
        """
        """
        if self.time_profile=="gaussian":
            t0=self.time_fwhm/(2 * _np.sqrt(_np.log(2)))
            S0t=t0 * _np.sqrt(_np.pi)
            return S0t
        else:
            raise NameError("Unknown laser time profile name.")

    def spaceIntegralDouble(self):
        """
        """
        if self.space_profile=="gaussian":
            r0=self.space_fwhm/(2 * _np.sqrt(_np.log(2)))
            S0r=_np.pi * r0**2
            return S0r
        elif self.space_profile=="top-hat":
            return _np.pi*self.space_radius**2
        else:
            raise NameError("Unknown laser space profile name.")



class Laser(object):
    """
    Class for defining laser characteristics. It needs to take as arguments

    Parameters
    ---------
    name, string
    Laser name

    wavelength, float

    energy, float
    Total energy of the laser pulse

    profile, object


    Attributes
    ----------

    Methods
    -------

    """
    def __init__(self,name,wavelength,energy,Profile,**kwargs):
        self.name       = name
        self.wavelength = wavelength
        self.energy     = energy

        self.profile    = Profile

    def pulsation(self):
        return 2*_np.pi*_u.c/self.wavelength

    def numberDensityCritical(self):
        return _u.m_e*_u.epsilon_0*(self.pulsation()/_u.e)**2

    def power(self,r=0*_u('m'),t=0*_u('s')):
        return self.energy/self.profile.timeIntegral() * self.profile.timeEnvelope(t) * self.profile.spaceEnvelope(r)

    def intensity(self,r=0*_u('m'),t=0*_u('s')):
        return self.power(r,t)/self.profile.spaceIntegralDouble()

    def intensityNormalized(self):
        """
        Return the normalized laser intensity.

        .. math:
            $a_0 = 0.85 \times \sqrt{I_{18} \lambda_{\mu}^2}$
            with $a_0$ the normalized laser intensity,
            $I_{18}$ the laser peak intensity in $10^{18} W.cm^{-2}$
            and $\lambda_{\mu}$ the laser wavelength in $10^{-6} m$.
        """
        return 0.85*_np.sqrt(\
                (self.intensity(r=0*_u('m'),t=0*_u('s')).to('W/cm**2')*(self.wavelength.to('um'))**2)\
                /(1.e18 * _u('W*um**2/cm**2')))

    def envelope(self,r,t):
        return self.intensity(t=0*_u('s'),r=0*_u('m'))*self.profile.spaceEnvelope(r) * self.profile.timeEnvelope(t)

    def timeChirp(self,t,phase=0.0 *_u('deg')):
        return _np.sin(self.pulsation().to(t.units**-1) * t - phase)
