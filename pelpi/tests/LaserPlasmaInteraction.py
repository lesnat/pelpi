# coding:utf8
import sys
Modules_path="../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

class LaserPlasmaInteractionTest(object):
    def instanciateTest(self):
        self.laser      = Laser
        self.target     = Target

        self.updateParameters()

    def updateParameters(self):
        self.plasma     = PlasmaParameters(self)
        self.absorption = []
        self.model      = _m.Model
        self.electron   = Electron(self)
        # self.ion        = Ion(self)
        self.default_model={'':''}
        self.ne_over_nc = self.target.mat.ne/self.laser.nc
        self.ni_over_nc = self.target.mat.ni/self.laser.nc

    def getLaserAbsorptionEfficiency(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Model=_m.Model.Obvious(self)
            out  = Model.getLaserAbsorptionEfficiency()
        else:
            raise NameError("getLaserAbsorptionEfficiency : Unknown model name.")

        out.to_base_units()
        return out


    def getTargetConductivity(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Tec     = 1e-3
            logCoulomb = 5.
            Model=_m.Model.Obvious(self)
            self.Sigma  = Model.getTargetConductivity(Tec=Tec,logCoulomb=logCoulomb)
        else:
            raise NameError("getTargetConductivity : Unknown model name.")

        return self.Sigma


    class Electron(object):
        """

        """
        def __init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction
            self.hot    = self.Hot(self._lpi)
            # self.cold   = self.Cold(self._lpi)

        # TODO: here general stuff about all the electrons

        class Hot(object):
            """
            In UHI, super thermal electrons
            """
            def __init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction
                self.default_model={'numberTotal':'Bell1997','temperature':'Haines2009'}

            def numberTotal(self,model=None,**kwargs):
                """
                Return the total number of accelerated hot electrons [dimensionless].

                # Dimension
                # --------
                # dimensionless

                Arguments
                --------
                model, string (optional, default : "Bell1997")
                Name of the model.

                **kwargs, string(s)
                See "Parameter models" in section Models.
                For more informations about keyword arguments please refer to
                the documentation of the LaserPlasmaInteraction object.

                Models
                -----
                Bell1997 is a model created for ...
                Need a (hot electron?) temperature, electrical conductivity and laser absorption
                efficiency to work properly.
                Parameter models :
                    for the hot electron temperature : Teh_model (default : "Haines2009")
                    for conductivity : Sigma_model (default : "Obvious", i.e. Spitzer)
                    for absorption efficiency nu_laser_model (default : "...")

                Obvious is a simple estimation, for order of magnitude.
                It returns the total laser energy over the energy in hot electrons,
                estimate by 3/2 Teh.
                It needs a hot electron temperature to work properly.
                Parameter models :
                    for the hot electron temperature : Teh_model (default : "Haines2009")

                Examples
                -------
                n0 = lpi.electron.hot.numberTotal(model="Obvious")
                n0 = lpi.electron.hot.numberTotal(model="Bell1997", Teh_model="Wilks1992")
                """
                # if model is None:
                #     model=self._lpi.default_model[model]
                #
                # if model in available_models:
                #    Model=_m.model # TODO: how to do this ?
                #
                #    Model.needed_models # TODO: do something like this for giving default behaviour
                #
                #     Model.checkHypotheses()
                #     return Model.numberTotal(**kwargs).to('dimensionless') # TODO: with this, need to put default behaviour into Model.py
                # else:
                #     raise NameError("Unknown model name.")


                # available_models=["Bell1997","Obvious"]
                # TODO: argument loop=True -> loop over all the models with a checkHypotheses and try, except for getting the max value for ex. (func=max in arguments and return func(list))
                # TODO: generic procedure : testing if in available_models and generic checkHypotheses + return model(**kwargs) ?
                if model=="Bell1997":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
                    nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
                    Model   = _m.Model.Bell1997(self)
                    Model.checkHypotheses()
                    nehTot = Model.numberTotal(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet
                elif model=="Obvious":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Model=_m.Model.Obvious(self)
                    nehTot = Model.numberTotal(Teh)
                else:
                    raise NameError("Unknown model name.")

                return nehTot

            def lengthCaracDepth(self,model="Bell1997",**kwargs):
                """
                """
                if model=="Bell1997":
                    Teh     = self.temperature(kwargs.get('Teh_model','Haines2009'))
                    Sigma   = self.getTargetConductivity(kwargs.get('Sigma_model','Obvious'))
                    nu_laser = self.getLaserAbsorptionEfficiency(kwargs.get('nu_laser_model','Obvious'))
                    Model   = _m.Model.Bell1997(self)
                    Model.checkHypotheses()
                    zeh = Model.lengthCaracDepth(Teh,Sigma,nu_laser) # self. ou pas ? savoir si sauvegardé ds objet

                return zeh

            def temperature(self,model="Haines2009"):
                """
                Return the hot electron temperature.

                Arguments
                --------
                model, string (optional, default : "Haines2009")
                Name of the model.

                Models
                -----
                Beg1997 is an empirical model ...
                Based on the reference

                Haines2009 is a theoretical model ...
                Based on the reference

                Wilks1992 is an empirical model
                Based on the reference
                """
                dim='temperature'
                if model is None:
                    model=self._lpi.default_model[dim]

                if model in available_models:
                    Model=_m.model # TODO: how to do this ?

                    Model.checkHypotheses()
                    return Model.numberTotal(**kwargs).to(dim)
                else:
                    raise NameError("Unknown model name.")

                # if model=="Beg1997":
                #     Model=_m.Model.Beg1997(self)
                #     # Model.checkHypotheses()
                #     out = Model.temperature()
                # elif model=="Haines2009":
                #     Model=_m.Model.Haines2009(self)
                #     out = Model.temperature()
                # elif model=="Wilks1992":
                #     Model=_m.Model.Wilks1992(self)
                #     out = Model.temperature()
                # else:
                #     raise NameError("Unknown model name. Please refer to the documentation.")
                #
                # return out.to(_pu['temperature'])

            def timeInteractionMax(self,verbose=True):
                """
                """
                return 0.

            def lengthInteractionMax(self,verbose=True):
                return 0.
