#coding:utf8
import numpy as _np
from . import unit
from . import prefered_unit as _pu


__all__ = ["Profile","Laser"]

class Profile(object):
    """
    class for defining pulse profile envelope
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

    Arguments
    ---------
    name, string
    Laser name

    wavelength, float

    energy, float
    Total energy of the laser pulse

    time_profile, string
    Temporal profile of the pulse
    Available profiles :
        "gaussian", for a gaussian pule.
        You must define the time_fwhm variable for setting the time full width half maximum

        "supergaussian" ?

    space_profile, string
    Spatial profile of the pulse (waist).
    Available profiles :
        "gaussian", for a gaussian pule.
        You must define the space_fwhm variable for setting the spatial full width half maximum (waist)

        "supergaussian" ?

    contrast_1ps, float
    Contrast of the pulse (à quel temps ?)

    polarization=[0,1,0],

    direction=[0,0,1],

    angle=0.

    Attributes
    ----------

    Methods
    -------




    Notes
    -----
    """
    def __init__(self,name,wavelength,energy,contrast_1ps,\
        Profile,\
        polarization,direction,angle,**kwargs):

        self.name       = name
        self.wavelength = wavelength
        self.energy     = energy
        self.contrast_1ps   = contrast_1ps       # TODO: see if not 1ps
        self.polarization = polarization         # TODO: see for dimensionless

        self.profile    = Profile

        self.direction      = direction
        self.angle          = angle


    def pulsation(self):
        return 2*_np.pi*unit.c/self.wavelength

    def numberDensityCritical(self):
        return unit.m_e*unit.epsilon_0*(self.pulsation()/unit.e)**2

    def power(self,r=0*unit('m'),t=0*unit('s')):
        return self.energy/self.profile.timeIntegral() * self.profile.timeEnvelope(t) * self.profile.spaceEnvelope(r)

    def intensity(self,r=0*unit('m'),t=0*unit('s')):
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
                (self.intensity(r=0*unit('m'),t=0*unit('s')).to('W/cm**2')*(self.wavelength.to('um'))**2)\
                /(1.e18 * unit('W*um**2/cm**2')))


    def envelope(self,r,t):
        return self.intensity(t=0*unit('s'),r=0*unit('m'))*self.profile.spaceEnvelope(r) * self.profile.timeEnvelope(t)

    def timeChirp(self,t,phase=0.0 *unit('deg')):
        return _np.sin(self.pulsation().to(t.units**-1) * t - phase)

    #
    # def plot(self):
    #     import matplotlib.pyplot as plt
    #     t=_np.arange(-self.profile.timeIntegral().to('s')/unit.s,self.profile.timeIntegral().to('s')/unit.s,(2*_np.pi/10)*(1/self.wl).to('s')/unit.s) *unit.s
    #     r=_np.arange(-2*self.space_fwhm.to('m')/unit.m,2*self.space_fwhm.to('m')/unit.m,(2*_np.pi/10)*(unit.c/self.wl).to('m')/unit.m) * unit.m
    #     self.t = t
    #     self.r = r # TODO: a supprimer quand méthode OK
    #
    #     plt.subplot(221)
    #     plt.plot(self.pulseEnv(r,0*unit('s')),r)
    #     plt.ylim(ymin=min(r.magnitude),ymax=max(r.magnitude))
    #     plt.ylabel('r (m)') # TODO: voire pour automatiser unités
    #
    #     # plt.subplot(222)
    #     # gpulseEnv=_np.array([self.pulseEnv(e.magnitude,t.magnitude)*self.pulseChirp(t.magnitude) for e in r]) # TODO: broken
    #     # gt,gr=_np.meshgrid(t.magnitude,r.magnitude)
    #     # plt.pcolor(gt,gr,gpulseEnv)
    #
    #     plt.subplot(224)
    #     plt.plot(t,self.pulseEnv(0*unit('m'),t)*self.pulseChirp(t))
    #     plt.xlim(xmin=min(t.magnitude),xmax=max(t.magnitude))
    #     plt.xlabel('t (s)')
    #
    #     plt.legend()
    #     plt.show()
