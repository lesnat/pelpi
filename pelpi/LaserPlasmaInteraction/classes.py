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
    Laser : object
        Instanciated ``pelpi.Laser`` object
    Target : object
        Instanciated ``pelpi.Target`` object

    Attributes
    ----------
    laser : sub-module
        The ``pelpi.Laser`` object given as argument when the class was declared.
    target : sub-module
        The ``pelpi.Target`` object given as argument when the class was declared.
    plasma : sub-module
        Contains usual plasma parameters.
    model : sub-module
        Contains the all the available models.

    Notes
    -----
    result of arguments (*args) in methods
    +++++++++++++++++++++++++++++++++++
    Some models may need optional parameters, such as electron hot temperature
    or laser absorption efficiency for complete the calculus.
    These parameters can be choosen by the user (for order of magnitude) or
    calculated by other models and passed as argument.
    Please refer to the method documentation for more informations.
    """

    model      = _m # public attribute

    def __init__(self,Laser,Target):
        self.laser      = Laser
        self.target     = Target
        self.plasma     = self._PlasmaParameters(self)
        self.electron   = self._Electron(self)
        # self.ion        = Ion(self)


    class _Laser(_PelpiObject):
        """
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction

            # self._user_values=self._lpi.laser._user_values
            #
            # exclude=['set_default','get_default']
            # for var in dict(self._lpi.laser):
            #     if var[0]!='_' and var not in exclude:
            #         self.__dict__[var]=getattr(self._lpi.laser,var)
            #
            # self._setMethodsToDict()

            # Automatically add all new methods to laser object
            # for model in self.__dict__.keys():
            #     _addMethod(self._lpi.laser, self, model)

            self._lpi.laser.efficiency_absorption = self.efficiency_absorption #TODO: on laser or e- ?

        def efficiency_absorption(self,model,**kwargs): # TODO: what this model is about ? hot electrons ? ions ? ...
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


    class _Target(_PelpiObject):
        """
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction

            # Automatically add all new methods to laser object
            # for model in self.__dict__.keys():
            #     _addMethod(self._lpi.laser, self, model)

            self._lpi.target.conductivity = self.conductivity

            # add targetdensitynormalized


        def conductivity(self,model,**kwargs): # TODO: in target or e- ?
            """
            Return an estimate of the target electric conductivity.

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
            dimension='conductivity'

            estimate=_Estimate(self._lpi,model_name=model,available_models=available_models)
            return estimate.result(method_name='target_conductivity',dimension=dimension,**kwargs)

    class _Electron(_PelpiObject):
        """

        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction
            self.hot    = self._Hot(self._lpi)
            # self.cold   = self.Cold(self._lpi)

        # TODO: here general stuff about all the electrons
        # TODO: add number density ?

        class _Hot(_PelpiObject):
            """
            In UHI, super thermal electrons
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
        Comment faire pour utiliser une température autre que Te_pond ?
        via meilleure estimation de la température si abso != JxB ou donner le choix ?
        Passer tout ca en méthodes ?
        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi             = LaserPlasmaInteraction
            self.electron         = self._Electron(self._lpi)
            self.ion              = self._Ion(self._lpi)

        # def updateParameters(self): # TODO; convert to methods
        #     self.wpe        = 0.0 # Electron plasma frequency
        #     self.wpi        = 0.0 # Ion plasma frequency
        #     self.lambda_De  = 0.0 # Debye length
        #     self.vTe        = 0.0 # Electron thermal velocity
        #     self.vTi        = 0.0 # Ion thermal velocity
        #     self.vA         = 0.0 # Alfven velocity
        #     self.EFermi     = 0.0
        #
        #

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
                Plasma pulsation of electrons : 1/time quantity

                Notes
                -----
                The Landau length is defined as

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
                Plasma pulsation of ions : 1/time quantity

                Notes
                -----
                The Landau length is defined as

                .. math:: \omega_{pe} = \sqrt{\\frac{Z^2 n_i e^2}{m_i \epsilon_0}}
                """
                ni  = self._lpi.target.material.ion.number_density()
                Z   = self._lpi.target.material.Z()
                mi  = self._lpi.target.material.atomic_mass()

                wpi = _np.sqrt((ni * (Z * _u.e)**2)/(mi * _u.epsilon_0))
                return wpi.to(_du['pulsation'])
