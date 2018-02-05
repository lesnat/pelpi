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
        dx_target   = 3.4 * self._lpi.plasma.electron.length_Debye(temperature).to(_du['length'])
        dx_laser    = (self._lpi.laser.wavelength()/10).to(_du['length'])
        return min(dx_laser,dx_target)

    def time_step(self,temperature,CFL=True):
        if CFL:
            return (1/_np.sqrt(2) *self.length_cell(temperature)/_u.c).to(_du['time'])
        else:
            return (self.length_cell(temperature)/_u.c).to(_du['time'])

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

    def length_simulation(self):
        return 64*_u('um')

    def length_patch(self,number_patches):
        Lsim = self.length_simulation()
        return Lsim/number_patches

    # def number_patch(self,temperature):
    #     npatches = [Lsim/float(2**n) for n in range(10)]
    #     return npatches

    class _CodeUnit(_PelpiObject):
        """
        Sub-class for

        """ # TODO: add pint unit for CU conversion ?
        def __init__(self,LaserPlasmaInteraction,reference_pulsation):
            self._lpi   = LaserPlasmaInteraction
            self._reference_pulsation = reference_pulsation

        def pulsation(self):
            return self._reference_pulsation

        def length(self):
            Lr = _u.c/self.pulsation()
            return Lr.to(_du['length'])

        def time(self):
            Tr = 1/self.pulsation()
            return Tr.to(_du['time'])

        def electric_field(self):
            Er = _u.m_e * _u.c * self.pulsation()/_u.e
            return Er.to(_du['electric_field'])

        def magnetic_field(self):
            Br = _u.m_e * self.pulsation()/_u.e
            return Br.to(_du['magnetic_field'])

        def number_density(self):
            Nr = self._lpi.laser.electron.number_density_critical() # TODO: change by the real calculus (if no laser)
            return Nr.to(_du['number_density'])

        def current(self):
            Jr = _u.c * _u.e * self.number_density()
            return Jr.to(_du['current'])

        def energy(self):
            Kr = 1 * _u.m_e * _u.c**2
            return Kr.to(_du['energy'])

        def momentum(self):
            Pr = 1 * _u.m_e * _u.c
            return Pr.to(_du['momentum'])
