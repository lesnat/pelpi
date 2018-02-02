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

    def length_cell(self,temperature):
        """
        Tskahya et al.
        """
        dx_target   = 3.4 * self._lpi.plasma.electron.length_Debye(temperature).to(_pu['length'])
        dx_laser    = (self._lpi.laser.wavelength()/10).to(_pu['length'])
        return min(dx_laser,dx_target)

    def time_step(self,temperature,CFL=True):
        if CFL:
            return (1/_np.sqrt(2) *self.length_cell(temperature)/_u.c).to(_pu['time'])
        else:
            return (self.length_cell(temperature)/_u.c).to(_pu['time'])

    # def CFL(self,length_cell=None,time_step=None,*arg):
    #     if length_cell==None:
    #         dx=self.length_cell(*arg)
    #     if time_step==None:
    #         dt=self.time_step(*arg)
    #     return (dx/dt * 1/_u.c).to('')

    def space_resolution(self,temperature):
        return 1/self.length_cell(temperature=temperature)

    def time_resolution(self,temperature,CFL=True):
        return 1/self.time_step(temperature=temperature,CFL=CFL)

    class _CodeUnit(_PelpiObject):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,reference_pulsation):
            self._lpi   = LaserPlasmaInteraction
            self._reference_pulsation = reference_pulsation

        def reference_pulsation(self):
            return self._reference_pulsation

        def length(self):
            return (_u.c/self.reference_pulsation()).to(_pu['length'])

        def time(self):
            return (1/self.reference_pulsation()).to(_pu['time'])

        def pulsation(self):
            return self.reference_pulsation().to(_pu['pulsation'])

        def electric_field(self):
            # return (_u.m_e * _u.c * self.reference_pulsation()/_u.e).to(_pu['electric field'])
            return (_u.m_e * _u.c * self.reference_pulsation()/_u.e).to_base_units()

        def magnetic_field(self):
            # return (_u.m_e * self.reference_pulsation()/_u.e).to(_pu['magnetic field'])
            return (_u.m_e * self.reference_pulsation()/_u.e).to_base_units()

        def number_density(self):
            return self._lpi.laser.numberDensityCritical()

        def current(self):
            # return (_u.c * _u.e * self.numberDensity()).to(_pu['current'])
            return (_u.c * _u.e * self.numberDensity()).to_base_units()

        def energy(self):
            return (_u.m_e * _u.c**2).to(_pu['energy'])

        def momentum(self):
            # return (_u.m_e * _u.c).to(_pu['momentum'])
            return (_u.m_e * _u.c).to_base_units()
