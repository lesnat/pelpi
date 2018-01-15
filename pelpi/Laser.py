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
        self.P0             = self.energy/self.getTimeIntegral()
        self.I0             = self.P0/self.getSurfaceIntegral()
        self.a0             = 0.85*_np.sqrt((1e-4*self.I0*self.wavelength**2)/(1.e18 * unit.W*unit.m**-2 *1.e-12*unit.m**2))

        self.wl             = 2*_np.pi*unit.c/self.wavelength
        self.nc             = unit.m_e*unit.epsilon_0*(self.wl/unit.e)**2 # m^-3

        self.pulseEnv       = lambda r,t: self.I0.to('W/cm**2')/unit('W/cm**2') *  self.spulseEnv(r) * self.tpulseEnv(t) # TODO: a modif?
        self.pulseChirp     = lambda t: _np.sin(self.wl*t)

    def tpulseEnv(self,t):
        if self.tprofile=="gaussian":
            return _np.exp(-(2*_np.sqrt(_np.log(2))*t/self.tfwhm)**2)

    def spulseEnv(self,r):
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

    def getTimeIntegral(self,r=0.0):
        """
        """
        # TODO: Return total time ? 1/e time ? 1/2 time ?
        if self.tprofile=="gaussian":
            t0=self.tfwhm/(2 * _np.sqrt(_np.log(2)))
            S0t=t0 * _np.sqrt(_np.pi)
            return S0t
        else:
            raise NameError("Unknown laser temporal profile name.")

    def getSurfaceIntegral(self,t=0.0):
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

    def getInfo(self):
        txt  = " \n"
        txt += " Laser parameters :\n"
        txt += " ########################################## \n"
        txt += " name               :      "+self.name+"\n"
        txt += " wavelength         :      "+str(self.wavelength.to(_pu['length']))+" \n"
        txt += " tprofile           :      "+self.tprofile+" \n"
        txt += " tfwhm              :      "+str(self.tfwhm.to(_pu['time']))+" \n"
        txt += " sprofile           :      "+self.sprofile+" \n"
        txt += " sfwhm              :      "+str(self.sfwhm.to(_pu['length']))+" \n"
        txt += " contrast           :      "+str(self.contrast)+"\n"
        txt += " energy             :      "+str(self.energy.to(_pu['energy']))+" \n"
        txt += " direction (x,y,z)  :      "+str(self.direction)+"\n"
        txt += " angle              :      "+str(self.angle.to(_pu['angle']))+" \n"
        txt += " I0                 :      "+str(self.I0.to(_pu['intensity']))+" \n"
        txt += " P0                 :      "+str(self.P0.to(_pu['power']))+" \n"
        txt += " a0                 :      "+str(self.a0.to_base_units())+"\n"
        txt += " wl                 :      "+str(self.wl.to(_pu['pulsation']))+" \n"
        txt += " nc                 :      "+str(self.nc.to(_pu['density']))+" \n"
        txt += " ########################################## \n"
        return txt


    def plot(self):
        import matplotlib.pyplot as plt
        t=_np.arange(-self.getTimeIntegral().to('s')/unit.s,self.getTimeIntegral().to('s')/unit.s,(2*_np.pi/10)*(1/self.wl).to('s')/unit.s) *unit.s
        r=_np.arange(-2*self.sfwhm.to('m')/unit.m,2*self.sfwhm.to('m')/unit.m,(2*_np.pi/10)*(unit.c/self.wl).to('m')/unit.m) * unit.m
        self.t = t
        self.r = r # TODO: a supprimer quand méthode OK

        plt.subplot(221)
        plt.plot(self.pulseEnv(r,0*unit('s')),r)
        plt.ylim(ymin=min(r.magnitude),ymax=max(r.magnitude))
        plt.ylabel('r (m)') # TODO: voire pour automatiser unités

        # plt.subplot(222)
        # gpulseEnv=_np.array([self.pulseEnv(e.magnitude,t.magnitude)*self.pulseChirp(t.magnitude) for e in r]) # TODO: broken
        # gt,gr=_np.meshgrid(t.magnitude,r.magnitude)
        # plt.pcolor(gt,gr,gpulseEnv)

        plt.subplot(224)
        plt.plot(t,self.pulseEnv(0*unit('m'),t)*self.pulseChirp(t))
        plt.xlim(xmin=min(t.magnitude),xmax=max(t.magnitude))
        plt.xlabel('t (s)')

        plt.legend()
        plt.show()
