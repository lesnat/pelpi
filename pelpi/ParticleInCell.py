#coding:utf8
from . import unit as _u
import numpy as _np

class ParticleInCell(object):
    # Estimations
    # Faire un dictionnaire pour choisir unités et ajouter verbosities pour afficher calculs intermédiaires ?
    def __init__(self,LaserPlasmaInteraction):
        lpi             = LaserPlasmaInteraction

        self.Wr         = lpi.laser.wl
        self.Lr         = _u.c/self.Wr
        self.Tr         = 1/self.Wr
        self.Er         = _u.m_e * _u.c * self.Wr/_u.e
        self.Br         = _u.m_e * self.Wr/_u.e
        self.Nr         = lpi.laser.nc
        self.Jr         = _u.c * _u.e * self.Nr
        self.Kr         = _u.m_e * _u.c**2
        self.Pr         = _u.m_e * _u.c

        self.dx_laser   = lpi.laser.wavelength/10 # voire pour les 2 pi
        self.dx_target  = (0.1 * (lpi.laser.wavelength/2*_np.pi) * \
            _np.sqrt(lpi.Teh*511/lpi.ne_over_nc))
        self.dx         = max(self.dx_laser,self.dx_target)
        self.dt         = self.dx/_np.sqrt(2)
        self.CFL        = self.dt/self.dx
        if self.CFL>1.0:
            print("Warning ! CFL condition not respected")

        self.LppTot     = -_np.log(0.01/lpi.ne_over_nc)*lpi.target.geom.Lpp

        self.resx       = 1/self.dx
        self.rest       = 1/self.dt
        self.Lsim_laser = _u.c * 2 * lpi.laser.tfwhm + lpi.target.geom.width + self.LppTot
        self.Lsim_lpi   = lpi.getInteractionLengthMax() + lpi.target.geom.width + self.LppTot
        self.Lsim       = max(self.Lsim_laser,self.Lsim_lpi)
        self.Tsim_laser = 2 * (self.Lsim - lpi.target.geom.width)/_u.c # ! Fonctionne si le laser ne pénètre pas dans la cible !
        self.Tsim_lpi   = lpi.getInteractionTimeMax() + (self.Lsim - lpi.target.geom.width)/_u.c
        self.Tsim       = max(self.Tsim_laser,self.Tsim_lpi)

        self.Nynquist = 0. # facteur de nynquist pour echantillonage des diags

    def getInfo(self): # conversions ici ?
        txt  = " \n"
        txt += " Particle In Cell code parameters :\n"
        txt += " ########################################## \n"
        # txt += " dx                 :      "+un.sciFormat(self.dx)+" m\n"
        # txt += " dx                 :      "+un.sciFormat(self.dx/self.Lr)+" Lr\n"
        # txt += " 2pi/dx             :      "+un.sciFormat(2*_np.pi/self.dx)+" m^-1\n"
        # txt += " 2pi/dx             :      "+un.sciFormat(self.Lr*2*_np.pi/self.dx)+" Lr^-1\n"
        # txt += " dt                 :      "+un.sciFormat(self.dt)+" s\n"
        # txt += " dt                 :      "+un.sciFormat(self.dt/self.Tr)+" Tr\n"
        # txt += " resx               :      "+un.sciFormat(self.resx)+" m^-1\n"
        # txt += " resx               :      "+un.sciFormat(self.resx*self.Lr)+" Lr^-1\n" # Revoir
        # txt += " rest               :      "+un.sciFormat(self.rest)+" s^-1\n"
        # txt += " rest               :      "+un.sciFormat(self.rest*self.Tr)+" Tr^-1\n" # Revoir
        # txt += " CFL                :      "+un.sciFormat(self.CFL)+" \n"
        # txt += " Lsim_laser         :      "+un.sciFormat(self.Lsim_laser)+" m\n"
        # txt += " Lsim_lpi           :      "+un.sciFormat(self.Lsim_lpi)+" m\n"
        # txt += " Lsim               :      "+un.sciFormat(self.Lsim)+" m\n"
        # txt += " Tsim_laser         :      "+un.sciFormat(self.Tsim_laser)+" s\n"
        # txt += " Tsim_lpi           :      "+un.sciFormat(self.Tsim_lpi)+" s\n"
        # txt += " Tsim               :      "+un.sciFormat(self.Tsim)+" s\n"
        txt += " ########################################## \n"

        return txt

    def convertSItoCU(self,var,unit):
        if unit=="m":
            return var * w_l/c
        elif unit=="s":
            return var * w_l
        elif unit=="MeV":
            return var * 1e6*e/(m_e*c**2)
        elif unit=="J":
            return var / (m_e*c**2)
        elif unit=="m^-3":
            return var / (epsilon_0*m_e*(w_l/e)**2)
        else:
            print("Unknown unit : "+unit)

    class codeUnit(object):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,referenceAngularFrequency):
            self._lpi   = LaserPlasmaInteraction
            self.referenceAngularFrequency = referenceAngularFrequency

        def length(self):
            return _u.c/self.referenceAngularFrequency.to('1/s')
