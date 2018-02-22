#coding:utf8

from ._global import *
from ._tools import _PelpiObject

class ParticleInCell(_PelpiObject):
    """
    Class for estimate Particle-In-Cell numerical parameters.
    
    Parameters
    ----------
    lpi : object
        pelpi ``LaserPlasmaInteraction`` instance
        
    Attributes
    ----------
    lpi : object
        Input lpi instance
    code : object
        Contains specific code calculations
    """
    def __init__(self,lpi):
        # Test user input
        self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")

        # Initialize default dict
        self._initialize_defaults()

        # Save reference to lpi instance into attributes
        self.lpi       = lpi

        # Instanciate sub-class
        self.code       = self._Code(self.lpi)

    def length_cell(self,lim,temperature=None):
        """
        Returns
        -------
        Maximal cell length to use, according to the choosen limitation (target, laser or both).

        
        Parameters
        ----------
        lim : str
            Which limitation to choose
        temperature : energy Quantity, optional
            Choosen temperature for the estimate
            
        Notes
        -----
        Available `lim` parameters are
        
        "target", for a result depending on the target limitation of cell length (3.4 Debye length)
        In this case `temperature` might be defined.
        
        "laser", for a result depending on the laser limitation of cell length (wavelength / 10)
        
        "both", for taking the minimum of the two previous results.
        `temperature` might then also be defined.
 
        More informations can be found in Tskahya et al.
        
        Examples
        --------
        TODO
        """
        if self.default['length_cell'] is not None:
            return self.default['length_cell']
        else:
            if lim =='target':
                dx = 3.4 * self.lpi.plasma.electron.length_Debye(temperature)
            elif lim =='laser':
                dx = self.lpi.laser.wavelength()/10.0
            elif lim =='both':
                dx = min(self.length_cell('target',temperature),self.length_cell('laser'))
            else:
                raise NameError("Unknown value of parameter 'lim'.")
            return dx.to(_du['length'])

    def time_step(self,lim,CFL,temperature=None):
        """
        Returns
        -------
        Maximal time step to use, according to the choosen limitation (target, laser or both)
        and if the Courant–Friedrichs–Lewy condition might be satisfied.
        
        Parameters
        ----------
        lim : str
            Which limitation to choose
        CFL : bool
            True if CFL condition might be satisfied, False otherwise
        temperature : energy Quantity, optional
            Choosen temperature for the estimate
            
        Notes
        -----
        time_step is calculated via the length_cell method, so see length_cell documentation
        for more information about `lim` and `temperature` parameters.
        """
        if self.default['time_step'] is not None:
            return self.default['time_step']
        else:
            if CFL:
                dt = 1/_np.sqrt(2) *self.length_cell(lim,temperature)/_u.c
            else:
                dt = self.length_cell(lim,temperature)/_u.c
            return dt.to(_du['time'])

    def space_resolution(self,lim,temperature=None):
        """
        Returns
        -------
        Minimal space resolution to use, according to the choosen limitation (target, laser or both).
        
        Parameters
        ----------
        lim : str
            Which limitation to choose
        temperature : energy Quantity, optional
            Choosen temperature for the estimate
            
        Notes
        -----
        space_resolution is calculated via the length_cell method, so see length_cell documentation
        for more information about `lim` and `temperature` parameters.
        """
        if self.default['space_resolution'] is not None:
            return self.default['space_resolution']
        else:
            resx = 1/self.length_cell(lim,temperature)
            return resx # no unit conversion because already converted in length_cell

    def time_resolution(self,lim,CFL,temperature=None):
        """
        Returns
        -------
        Minimal time resolution to use, according to the choosen limitation (target, laser or both)
        and if the Courant–Friedrichs–Lewy condition might be satisfied.
        
        Parameters
        ----------
        lim : str
            Which limitation to choose
        CFL : bool
            True if CFL condition might be satisfied, False otherwise
        temperature : energy Quantity, optional
            Choosen temperature for the estimate
            
        Notes
        -----
        time_resolution is calculated via the length_cell method, so see length_cell documentation
        for more information about `lim` and `temperature` parameters.
        """
        if self.default['time_resolution'] is not None:
            return self.default['time_resolution']
        else:
            rest = 1/self.time_step(lim,CFL,temperature)
            return rest # no unit conversion because already converted in time_step

    class _Code(_PelpiObject):
        """
        Contains specific code calculations.
        
        Parameters
        ----------
        lpi : object
            pelpi ``LaserPlasmaInteraction`` instance
            
        Attributes
        ----------
        smilei : object
            Tools for Smilei PIC code
        """
        def __init__(self,lpi):
            # Test user input
            self._check_input('lpi',lpi,"<class 'pelpi.lpi.LaserPlasmaInteraction'>")

            # Do not initialize default dict because there is no direct access to methods from this point

            # Instanciate sub-class
            wr              = lpi.laser.angular_frequency()
            self.smilei     = self._Smilei(wr)

        class _Smilei(_PelpiObject):
            """
            Smilei tools. Contains reference units and tools to optimize simulation time.
            
            Parameters
            ----------
            angular_frequency_reference : 1/time Quantity, optional
                Reference angular frequency.
            
            Notes
            -----    
            smilei object is automatically instanciated with the laser angular frequency as a reference frequency.
            This can be changed by setting a new value to pic.code.smilei.default['angular_frequency_reference']
            
            For more informations about Smilei PIC code and normalisation units, see 
            https://smileipic.github.io/Smilei/
            
            Default return of methods can be set in this object, 
            but as the aim of this object is to provide calculation of reference parameters,
            do not use it unless you know what you are doing.
            """
            # TODO: add pint unit for CU conversion ?
            # TODO: add patches & OMP/MPI optimization calculations
            def __init__(self,angular_frequency_reference):
                # Test user input
                self._check_input('angular_frequency_reference',angular_frequency_reference,type(_du['angular_frequency']))

                # Initialize default dict
                self._initialize_defaults(input_dict={'angular_frequency_reference':angular_frequency_reference})

            def angular_frequency(self):
                return self.default['angular_frequency_reference']

            def length(self):
                """
                Returns
                -------
                Smilei reference length : length Quantity
                """
                if self.default['length'] is not None:
                    return self.default['length']
                else:
                    Lr = _u.c/self.angular_frequency()
                    return Lr.to(_du['length'])

            def time(self):
                """
                Returns
                -------
                Smilei reference time : time Quantity
                """
                if self.default['time'] is not None:
                    return self.default['time']
                else:
                    Tr = 1/self.angular_frequency()
                    return Tr.to(_du['time'])

            def electric_field(self):
                """
                Returns
                -------
                Smilei reference electric field : Quantity
                """
                if self.default['electric_field'] is not None:
                    return self.default['electric_field']
                else:
                    Er = _u.m_e * _u.c * self.angular_frequency()/_u.e
                    return Er.to(_du['electric_field'])

            def magnetic_field(self):
                """
                Returns
                -------
                Smilei reference magnetic field : Quantity
                """
                if self.default['magnetic_field'] is not None:
                    return self.default['magnetic_field']
                else:
                    Br = _u.m_e * self.angular_frequency()/_u.e
                    return Br.to(_du['magnetic_field'])

            def number_density(self):
                """
                Returns
                -------
                Smilei reference number density : 1/length**3 Quantity
                """
                if self.default['number_density'] is not None:
                    return self.default['number_density']
                else:
                    Nr = _u.m_e * _u.epsilon_0 *(self.angular_frequency()/_u.e)**2
                    return Nr.to(_du['number_density'])

            def current(self):
                """
                Returns
                -------
                Smilei reference current : Quantity
                """
                if self.default['current'] is not None:
                    return self.default['current']
                else:
                    Jr = _u.c * _u.e * self.number_density()
                    return Jr.to(_du['current'])

            def energy(self):
                """
                Returns
                -------
                Smilei reference energy : energy Quantity
                """
                if self.default['energy'] is not None:
                    return self.default['energy']
                else:
                    Kr = 1 * _u.m_e * _u.c**2
                    return Kr.to(_du['energy'])

            def momentum(self):
                """
                Returns
                -------
                Smilei reference momentum : Quantity
                """
                if self.default['momentum'] is not None:
                    return self.default['momentum']
                else:
                    Pr = 1 * _u.m_e * _u.c
                    return Pr.to(_du['momentum'])
