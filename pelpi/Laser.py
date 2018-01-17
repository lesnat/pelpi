#coding:utf8
import numpy as _np
from . import unit
from . import prefered_unit as _pu


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

    tprofile, string
    Temporal profile of the pulse
    Available profiles :
        "gaussian", for a gaussian pule.
        You must define the tfwhm variable for setting the temporal full width half maximum

        "supergaussian" ?

    sprofile, string
    Spatial profile of the pulse (waist).
    Available profiles :
        "gaussian", for a gaussian pule.
        You must define the sfwhm variable for setting the spatial full width half maximum (waist)

        "supergaussian" ?

    contrast, float
    Contrast of the pulse (à quel temps ?)

    polar=[0,1,0],

    direction=[0,0,1],

    angle=0.

    Attributes
    ----------

    Methods
    -------




    Notes
    -----
    """
    def __init__(self,name,wavelength,energy,contrast,\
        tprofile,sprofile,\
        polar=[0,1,0],direction=[0,0,1],angle=0.*unit.deg,**kwargs):

        self.name       = name
        self.wavelength = wavelength
        self.energy     = energy
        self.contrast   = contrast
        self.polar      = polar         # TODO: voire pour mettre dimensionless
        self.tprofile   = tprofile
        self.tfwhm      = kwargs.get('tfwhm',None)
        self.sprofile   = sprofile
        self.sfwhm      = kwargs.get('sfwhm',None)
        self.radius     = kwargs.get('radius',None)
        # self.diameter   = kwargs.get('diameter',None)

        self.direction      = direction
        self.angle          = angle

        self.updateParameters()


    def updateParameters(self):

        self.pulseEnv       = lambda r,t: self.I0.to('W/cm**2')/unit('W/cm**2') *  self.profileEnvelopeSpatial(r) * self.profileEnvelopeTemporal(t) # TODO: a modif?
        self.pulseChirp     = lambda t: _np.sin(self.wl*t)

    def wavelength(self):
        return self.wavelength

    def pulsation(self):
        return 2*_np.pi*unit.c/self.wavelength()

    def densityCritical(self):
        return unit.m_e*unit.epsilon_0*(self.pulsation()/unit.e)**2

    def power(self,r=0*unit('m'),t=0*unit('s')):
        return self.energy()/self.integralTemporal() * self.profileEnvelopeTemporal(t) * self.profileEnvelopeSpatial(r)

    def intensity(self,r=0*unit('m'),t=0*unit('s')):
        return self.power(r,t)/self.integralSpatialSurface()

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
                (self.intensity(r=0*unit('m'),t=0*unit('s')).to('W/cm**2')*(self.wavelength().to('um'))**2)\
                /(1.e18 * unit('W/cm**2')))

    def profileEnvelopeTemporal(self,t):
        if self.tprofile=="gaussian":
            return _np.exp(-(2*_np.sqrt(_np.log(2))*t/self.tfwhm)**2)

    def profileEnvelopeSpatial(self,r):
        if self.sprofile=="gaussian":
            return _np.exp(-(2*_np.sqrt(_np.log(2))*r/self.sfwhm)**2)
        elif self.sprofile=="supergaussian":
            n=10
            return _np.exp(-(2*_np.sqrt(_np.log(2))*r/self.sfwhm)**(2*n))
        elif self.sprofile=="top-hat":
            if abs(r)<self.radius:
                return 1.0
            else:
                return 0.0

    def integralTemporal(self,r=0.0):
        """
        """
        # TODO: Return total time ? 1/e time ? 1/2 time ?
        if self.tprofile=="gaussian":
            t0=self.tfwhm/(2 * _np.sqrt(_np.log(2)))
            S0t=t0 * _np.sqrt(_np.pi)
            return S0t
        else:
            raise NameError("Unknown laser temporal profile name.")

    def integralSpatialSurface(self,t=0.0):
        """
        """
        # TODO: se démerder pour appeller cette méthode dans conversion en intensité ?
        if self.sprofile=="gaussian":
            r0=self.sfwhm/(2 * _np.sqrt(_np.log(2)))
            S0r=_np.pi * r0**2
            return S0r
        elif self.sprofile=="top-hat":
            return _np.pi*self.radius**2
        else:
            raise NameError("Unknown laser spatial profile name.")

    #
    # def plot(self):
    #     import matplotlib.pyplot as plt
    #     t=_np.arange(-self.integralTemporal().to('s')/unit.s,self.integralTemporal().to('s')/unit.s,(2*_np.pi/10)*(1/self.wl).to('s')/unit.s) *unit.s
    #     r=_np.arange(-2*self.sfwhm.to('m')/unit.m,2*self.sfwhm.to('m')/unit.m,(2*_np.pi/10)*(unit.c/self.wl).to('m')/unit.m) * unit.m
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
