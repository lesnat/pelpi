#coding:utf8

from .._global import *
from .._tools import _PelpiObject
from ..LaserPlasmaInteraction import model as _m

__all__ = ["LaserPlasmaInteraction"]

################################################################################
class LaserPlasmaInteraction(_PelpiObject):
    """
    Class for estimations in laser-plasma interaction.

    Parameters
    ----------
    laser : object
        Instanciated pelpi ``Laser`` object
    target : object
        Instanciated pelpi ``Target`` object

    Attributes
    ----------
    laser : object
        Input laser object
    target : object
        Input target object
    model : object
        Contains the all available models. Class attribute.
    plasma : object
        Contains usual plasma parameters
    electron : object
        Contains estimations about electrons
    


    Examples
    --------
    TODO


    Notes
    -----
    New methods in input objects
    ++++++++++++++++++++++++++++
    TODO    
    
    Keyword arguments (**kwargs) in estimation methods
    ++++++++++++++++++++++++++++++++++++++++++++++++++
    Even if the code structure permit not to give a lot of parameters
    to perform an estimate, some complex models may need several of them to give the result.
    
    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.
    
    To do this, pelpi needs the parameters to be defined explicitly, i.e. with the parameter
    name in the method call.
    
    Here is a quick example, assuming ``lpi`` is an instance of ``LaserPlasmaInteraction``
    
    >>> eh = lpi.electron.hot
    >>> # Define the laser absorption efficiency
    >>> eta_l = 0.1 * pp.unit('')
    >>> # Use a simple model to get a temperature estimate
    >>> Teh = eh.temperature(model='Haines2009')
    >>> # Here a more complex model needs a temperature & absorption efficiency to return a result
    >>> neh = eh.number_total(model="Common",temperature = Teh, absorption_efficiency = eta_l) # Works
    >>> neh = eh.number_total(model="Common", Teh, eta_l) # Do not works
    
    Refer to the desired method documentation for more informations about parameters of each model.
    
    """

    model      = _m # public attribute pointing to lpi models

    def __init__(self,laser,target):
        # Test user input
        self._check_input('laser',laser,"<class 'pelpi.Laser.classes.Laser'>")
        self._check_input('target',target,"<class 'pelpi.Target.classes.Target'>")
        
        # Initialize default dict
        self._initialize_defaults()
        
        # Save references to target & laser instances into attributes
        self.laser      = laser
        self.target     = target
        
        # Instanciate sub-classes
        self.plasma     = self._PlasmaParameters(self)
        self.electron   = self._Electron(self)
        # self.ion        = Ion(self)

    class _Electron(_PelpiObject):
        """
        Electrons properties.
        
        Attributes
        ----------
        hot : object
            Containing properties of super-thermal electrons, in Ultra-High Intensity regime
        """
        def __init__(self,LaserPlasmaInteraction):
            # No need to check input because this method is only called in Laser definition.
            
            # Initialise default dict
            self._initialize_defaults()
            
            # Save reference to LaserPlasmaInteraction instance in a private variable
            self._lpi   = LaserPlasmaInteraction
            
            # Instanciate sub-classes
            self.hot    = self._Hot(self._lpi)
            # self.cold   = self._Cold(self._lpi)
            
            # Add methods previously defined
            self.number_density = self._lpi.target.material.electron.number_density
            self.number_density_critical = self._lpi.laser.electron.number_density_critical


        def efficiency_absorption(self,model,**kwargs):
            """
            Return an estimate of the laser absorption efficiency into hot electrons ??.

            Arguments
            --------
            model, string
                Model name
            **kwargs,
                Model input parameters

            Models
            -----
            Common, a theoretical model for a rough estimate.
                Input parameters : ...

            Notes
            ----
            See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
            if you need more informations about the [Model] model.
            """
            available_models=["Common"]
            dimension='number'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.result(method_name='laser_efficiency_absorption',dimension=dimension,**kwargs)

        class _Hot(_PelpiObject):
            """
            Super-thermal electrons, in Ultra-High Intensity regime.
            """
            def __init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction
                self.default={'temperature':None}
                self._initialize_defaults()

            def number_total(self,model,**kwargs):
                """
                Return an estimate of the total hot electron number.

                Arguments
                --------
                model, string
                    Model name
                *args,
                    Model input parameters

                Models
                -----
                Common, a theoretical model for a rough estimate.
                    Input parameters : ...

                Notes
                ----
                See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
                if you need more informations about the [Model] model.
                """
                available_models=["Common"]
                dimension='number'

                estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
                return estimate.result(method_name='electron_number_total',dimension=dimension,**kwargs)

            def temperature(self,model,**kwargs):
                """
                Return an estimate of the hot electron temperature.

                Arguments
                --------
                model, string
                    Model name
                **kwargs,
                    Model input parameters

                Models
                -----
                Beg1997, an empirical model ...
                    Input parameters : None

                Haines2009, a theoretical model ...
                    Input parameters : None

                Wilks1992, a theoretical model
                    Input parameters : None

                Notes
                ----
                See pelpi.Model.LaserPlasmaInteraction.[Model] documentation
                if you need more informations about the [Model] model.
                """
                if self.default['temperature'] is not None:
                    return self.default['temperature']
                else:
                    temperature = self._estimate(self._lpi,model,'electron_hot_temperature',**kwargs)
                    return temperature.to(_du['temperature'])
                
                """
                dimension='temperature'
                available_models=["Beg1997","Haines2009","Wilks1992"]

                estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
                return estimate.result(method_name='electron_hot_temperature',dimension=dimension,**kwargs)
                """

    class _PlasmaParameters(_PelpiObject):
        """
        Class containing usual plasma parameters.
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi             = LaserPlasmaInteraction
            self.electron         = self._Electron(self._lpi)
            self.ion              = self._Ion(self._lpi)


        class _Electron(_PelpiObject):
            def __init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction

            def length_Debye(self,temperature):
                """
                Returns
                -------
                Debye length of electrons : length quantity

                Notes
                -----
                The Debye length is defined as

                .. math:: \lambda_{De} = \sqrt{\\frac{\epsilon_0 T_e}{n_e e^2}}
                """
                ne  = self._lpi.target.material.electron.number_density()
                Te  = temperature

                LDe = _np.sqrt((_u.epsilon_0 * Te)/(ne * _u.e**2))
                return LDe.to(_du['length'])


            def length_Landau(self,temperature):
                """
                Returns
                -------
                Landau length of electrons : length quantity

                Notes
                -----
                The Landau length is defined as

                .. math:: r_0 = \\frac{e^2}{4 \pi \epsilon_0 T_e}
                """
                Te  = temperature

                LLa = ((_u.e**2)/(4*_np.pi * _u.epsilon_0 * Te)) # TODO: OK ? check
                return LLa.to(_du['length'])

            def pulsation_plasma(self,temperature):
                """
                Returns
                -------
                Plasma pulsation of electrons : 1/time Quantity

                Notes
                -----
                The plasma pulsation of electrons is defined as follows

                .. math:: \omega_{pe} = \sqrt{\\frac{n_e e^2}{m_e \epsilon_0}}
                """
                ne  = self._lpi.target.material.electron.number_density()

                wpe = _np.sqrt((ne * _u.e**2)/(_u.m_e * _u.epsilon_0))
                return wpe.to(_du['pulsation'])

        class _Ion(_PelpiObject):
            def __init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction

            def pulsation_plasma(self):
                """
                Returns
                -------
                Plasma pulsation of ions : 1/time Quantity

                Notes
                -----
                The plasma pulsation of ions is defined as follows

                .. math:: \omega_{pi} = \sqrt{\\frac{Z^2 n_i e^2}{m_i \epsilon_0}}
                """
                ni  = self._lpi.target.material.ion.number_density()
                Z   = self._lpi.target.material.Z()
                mi  = self._lpi.target.material.atomic_mass()

                wpi = _np.sqrt((ni * (Z * _u.e)**2)/(mi * _u.epsilon_0))
                return wpi.to(_du['pulsation'])
