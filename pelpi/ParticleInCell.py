#coding:utf8
# from . import unit as _u
# import numpy as _np
from ._global import *

class ParticleInCell(object):
    # Estimations
    # Faire un dictionnaire pour choisir unités et ajouter verbosities pour afficher calculs intermédiaires ?
    def __init__(self,LaserPlasmaInteraction):
        self._lpi             = LaserPlasmaInteraction
        self.unit             = self._CodeUnit(self._lpi,self._lpi.laser.pulsation())

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

    def lengthCellMin(self,temperature):
        self.dx_laser   = self._lpi.laser.wavelength()/10 # voire pour les 2 pi
        ne = self._lpi.target.material.electronNumberDensity()/self._lpi.laser.numberDensityCritical()
        self.dx_target  = (0.1*_u('keV**-(1/2.)') * (self._lpi.laser.wavelength()) * \
        _np.sqrt(temperature.to('keV')/ne))
        self.dx         = max(self.dx_laser,self.dx_target)
        return self.dx
        # if _vb:
        #     print("verbose")


        return self.dx.to(_pu['length'])


    class _CodeUnit(object):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,referenceAngularFrequency):
            self._lpi   = LaserPlasmaInteraction
            self.referenceAngularFrequency = referenceAngularFrequency

        def lengthCell(self):
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
