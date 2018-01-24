#coding:utf8
# from . import unit as _u
# import numpy as _np
from .._global import *
from .._tools import _PelpiObject

class ParticleInCell(_PelpiObject):
    # Estimations
    # Faire un dictionnaire pour choisir unités et ajouter verbosities pour afficher calculs intermédiaires ?
    def __init__(self,LaserPlasmaInteraction):
        self._lpi             = LaserPlasmaInteraction
        self.code             = self._CodeUnit(self._lpi,self._lpi.laser.pulsation())

    def other(self):
        self.dt         = self.dx/_np.sqrt(2)
        self.CFL        = self.dt/self.dx
        if self.CFL>1.0:
            print("Warning ! CFL condition not respected")

        self.LppTot     = -_np.log(0.01/self._lpi.ne_over_nc)*self._lpi.target.geom.Lpp

        self.resx       = 1/self.dx
        self.rest       = 1/self.dt
        self.Lsim_laser = _u.c * 2 * self._lpi.laser.tfwhm + self._lpi.target.geom.width + self.LppTot
        self.Lsim_lpi   = self._lpi.getInteractionLengthMax() + self._lpi.target.geom.width + self.LppTot
        self.Lsim       = max(self.Lsim_laser,self.Lsim_lpi)
        self.Tsim_laser = 2 * (self.Lsim - self._lpi.target.geom.width)/_u.c # ! Fonctionne si le laser ne pénètre pas dans la cible !
        self.Tsim_lpi   = self._lpi.getInteractionTimeMax() + (self.Lsim - self._lpi.target.geom.width)/_u.c
        self.Tsim       = max(self.Tsim_laser,self.Tsim_lpi)

        self.Nynquist = 0. # facteur de nynquist pour echantillonage des diags

    def lengthCell(self,kind='min',temperature=None):
        """
        Tskahya et al.
        """
        if kind=="target":
            return 3.4 * self._lpi.plasma.electronLengthDebye(temperature).to(_pu['length'])
        if kind=="laser":
            return (self._lpi.laser.wavelength()/10).to(_pu['length'])
        if kind=="min":
            return min(self.lengthCell(kind="target",temperature=temperature),self.lengthCell(kind="laser"))
        else:
            raise NameError

    def timeStep(self,kind="min",CFL=True,temperature=None):
        if CFL:
            return (0.95*self.lengthCell(kind,temperature)/_np.sqrt(2)).to(_pu['time'])
        else:
            return (self.lengthCell(kind,temperature)/_u.c).to(_pu['time'])

    def spaceResolution(self,kind,temperature=None):
        return 1/self.lengthCell(kind=kind,temperature=temperature)

    def timeResolution(self,kind,temperature=None):
        return 1/self.timeStep()

    class _CodeUnit(_PelpiObject):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,referenceAngularFrequency):
            self._lpi   = LaserPlasmaInteraction
            self.referenceAngularFrequency = referenceAngularFrequency

        def length(self):
            return (_u.c/self.referenceAngularFrequency.to('1/s')).to(_pu['length'])
            #
            # self.Wr         = self._lpi.laser.wl
            # self.Lr         = _u.c/self.Wr
            # self.Tr         = 1/self.Wr
            # self.Er         = _u.m_e * _u.c * self.Wr/_u.e
            # self.Br         = _u.m_e * self.Wr/_u.e
            # self.Nr         = self._lpi.laser.nc
            # self.Jr         = _u.c * _u.e * self.Nr
            # self.Kr         = _u.m_e * _u.c**2
            # self.Pr         = _u.m_e * _u.c
