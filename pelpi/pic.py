#coding:utf8

from ._global import *
from ._tools import _PelpiObject

class ParticleInCell(_PelpiObject):
    """

    """
    def __init__(self,LaserPlasmaInteraction):
        # Test user input
        self._check_input('laser',laser,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")

        # Initialize default dict
        self._initialize_defaults()

        # Save references to target & laser instances into attributes
        self.lpi        = lpi

        # Instanciate sub-classes
        self.code       = self._Code(self)

    def length_cell(self,temperature):
        """
        Tskahya et al.
        """
        dx_target   = 3.4 * self._lpi.plasma.electron.length_Debye(temperature).to(_du['length'])
        dx_laser    = (self._lpi.laser.wavelength()/10).to(_du['length'])
        return min(dx_laser,dx_target)

    def time_step(self,temperature,CFL):
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

    def time_resolution(self,temperature,CFL):
        return 1/self.time_step(temperature=temperature,CFL=CFL)

    # def length_simulation(self):
    #     return 64*_u('um')
    #
    # def length_patch(self,number_patches):
    #     Lsim = self.length_simulation()
    #     return Lsim/number_patches

    # def number_patch(self,temperature):
    #     npatches = [Lsim/float(2**n) for n in range(10)]
    #     return npatches
    class _Code(_PelpiObject):
        """
        Code tools.
        """
        def __init__(self,LaserPlasmaInteraction):
            lpi             = LaserPlasmaInteraction
            wr              = lpi.laser.angular_frequency()
            self.smilei     = self._Smilei(lpi,wr)

        class _Smilei(_PelpiObject):
            """
            Smilei tools.

            """ # TODO: add pint unit for CU conversion ?
            def __init__(self,LaserPlasmaInteraction,angular_frequency_reference):
                self._lpi   = LaserPlasmaInteraction
                self._angular_frequency_reference = angular_frequency_reference

            def angular_frequency_reference(self):
                return self._angular_frequency_reference

            def length_reference(self):
                Lr = _u.c/self.angular_frequency_reference()
                return Lr.to(_du['length'])

            def time_reference(self):
                Tr = 1/self.angular_frequency_reference()
                return Tr.to(_du['time'])

            def electric_field_reference(self):
                Er = _u.m_e * _u.c * self.angular_frequency_reference()/_u.e
                return Er.to(_du['electric_field'])

            def magnetic_field_reference(self):
                Br = _u.m_e * self.angular_frequency_reference()/_u.e
                return Br.to(_du['magnetic_field'])

            def number_density_reference(self):
                Nr = self._lpi.laser.electron.number_density_critical() # TODO: change by the real calculus (if no laser)
                return Nr.to(_du['number_density'])

            def current_reference(self):
                Jr = _u.c * _u.e * self.number_density()
                return Jr.to(_du['current'])

            def energy_reference(self):
                Kr = 1 * _u.m_e * _u.c**2
                return Kr.to(_du['energy'])

            def momentum_reference(self):
                Pr = 1 * _u.m_e * _u.c
                return Pr.to(_du['momentum'])
