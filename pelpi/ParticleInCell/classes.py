#coding:utf8

from .._global import *
from .._tools import _PelpiObject

class ParticleInCell(_PelpiObject):
    """

    """
    def __init__(self,LaserPlasmaInteraction):
        self._lpi             = LaserPlasmaInteraction
        self.code             = self._CodeUnit(self._lpi,self._lpi.laser.pulsation())
        # self._autoconvert = True #TODO: variable for autoconvert to CU

    def other(self):
        self.LppTot     = -_np.log(0.01/self._lpi.ne_over_nc)*self._lpi.target.geom.Lpp

        self.Lsim_laser = _u.c * 2 * self._lpi.laser.tfwhm + self._lpi.target.geom.width + self.LppTot
        self.Lsim_lpi   = self._lpi.getInteractionLengthMax() + self._lpi.target.geom.width + self.LppTot
        self.Lsim       = max(self.Lsim_laser,self.Lsim_lpi)
        self.Tsim_laser = 2 * (self.Lsim - self._lpi.target.geom.width)/_u.c # ! Fonctionne si le laser ne pénètre pas dans la cible !
        self.Tsim_lpi   = self._lpi.getInteractionTimeMax() + (self.Lsim - self._lpi.target.geom.width)/_u.c
        self.Tsim       = max(self.Tsim_laser,self.Tsim_lpi)

        self.Nynquist = 0. # facteur de nynquist pour echantillonage des diags

    def lengthCell(self,temperature):
        """
        Tskahya et al.
        """
        dx_target   = 3.4 * self._lpi.plasma.electronLengthDebye(temperature).to(_pu['length'])
        dx_laser    = (self._lpi.laser.wavelength()/10).to(_pu['length'])
        return min(dx_laser,dx_target)

    def timeStep(self,temperature,CFL=True):
        if CFL:
            return (1/_np.sqrt(2) *self.lengthCell(temperature)/_u.c).to(_pu['time'])
        else:
            return (self.lengthCell(temperature)/_u.c).to(_pu['time'])

    # def CFL(self,lengthCell=None,timeStep=None,*arg):
    #     if lengthCell==None:
    #         dx=self.lengthCell(*arg)
    #     if timeStep==None:
    #         dt=self.timeStep(*arg)
    #     return (dx/dt * 1/_u.c).to('')

    def spaceResolution(self,temperature):
        return 1/self.lengthCell(temperature=temperature)

    def timeResolution(self,temperature,CFL=True):
        return 1/self.timeStep(temperature=temperature,CFL=CFL)

    class _CodeUnit(_PelpiObject):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,referenceAngularFrequency):
            self._lpi   = LaserPlasmaInteraction
            self._referenceAngularFrequency = referenceAngularFrequency

        def referenceAngularFrequency(self):
            return self._referenceAngularFrequency

        def length(self):
            return (_u.c/self.referenceAngularFrequency()).to(_pu['length'])

        def time(self):
            return (1/self.referenceAngularFrequency()).to(_pu['time'])

        def pulsation(self):
            return self.referenceAngularFrequency().to(_pu['pulsation'])

        def electricField(self):
            # return (_u.m_e * _u.c * self.referenceAngularFrequency()/_u.e).to(_pu['electric field'])
            return (_u.m_e * _u.c * self.referenceAngularFrequency()/_u.e).to_base_units()

        def magneticField(self):
            # return (_u.m_e * self.referenceAngularFrequency()/_u.e).to(_pu['magnetic field'])
            return (_u.m_e * self.referenceAngularFrequency()/_u.e).to_base_units()

        def numberDensity(self):
            return self._lpi.laser.numberDensityCritical()

        def current(self):
            # return (_u.c * _u.e * self.numberDensity()).to(_pu['current'])
            return (_u.c * _u.e * self.numberDensity()).to_base_units()

        def energy(self):
            return (_u.m_e * _u.c**2).to(_pu['energy'])

        def momentum(self):
            # return (_u.m_e * _u.c).to(_pu['momentum'])
            return (_u.m_e * _u.c).to_base_units()
