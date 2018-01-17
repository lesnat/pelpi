# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

import unittest

class LaserPlasmaInteractionTest(unittest.TestCase):
    def setUp(self):
        profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u.fs,
            space_profile   = "gaussian",
            space_fwhm      = 10*u.um
        )
        lasGG=pp.Laser(
            name       = "test",

            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            Profile    = profGG,

            contrast_1ps = 1e8,

            polarization = [0,1,0],

            direction  = [0,0,1],
            angle      = 0. * u.deg,
        )
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )
        geomBas = pp.Geometry(
            width=20 * u.um,
            Lpp=8 * u.um
        )
        targAlBas = pp.Target(matAl,geomBas)

        self.lpiGGAlBas = pp.LaserPlasmaInteraction(lasGG,targAlBas)

    def tearDown(self):
        del self.lpiGGAlBas

    def test_instanciateTest(self):
        profGG = pp.Profile(
            time_profile    = "gaussian",
            time_fwhm       = 30*u.fs,
            space_profile   = "gaussian",
            space_fwhm      = 10*u.um
        )
        lasGG=pp.Laser(
            name       = "test",

            wavelength = 0.8 * u.um,
            energy     = 2.0 * u.J,

            Profile    = profGG,

            contrast_1ps = 1e8,

            polarization = [0,1,0],

            direction  = [0,0,1],
            angle      = 0. * u.deg,
        )
        matAl  = pp.Material(
            name        = "Al",
            density     = 2.69890e3 * u.kg/u.m**3,
            atomic_mass = 26.98154 * u.u,
            Z           = 13,
            A           = 27,
        )
        geomBas = pp.Geometry(
            width=20 * u.um,
            Lpp=8 * u.um
        )
        targAlBas = pp.Target(matAl,geomBas)
        lpiGGAlBas = pp.LaserPlasmaInteraction(lasGG,targAlBas)

    # def test_updateParameters(self):
    #     self.plasma     = PlasmaParameters(self)
    #     self.absorption = []
    #     self.model      = _m.Model
    #     self.electron   = Electron(self)
    #     # self.ion        = Ion(self)
    #     self.default_model={'':''}
    #     self.ne_over_nc = self.target.mat.ne/self.laser.nc
    #     self.ni_over_nc = self.target.mat.ni/self.laser.nc

    def test_getLaserAbsorptionEfficiency(self,model="Obvious",**kwargs):
        """
        """
        if model=="Obvious":
            Model=_m.Model.Obvious(self)
            out  = Model.getLaserAbsorptionEfficiency()
        else:
            raise NameError("getLaserAbsorptionEfficiency : Unknown model name.")

        out.to_base_units()
        return out


    def test_getTargetConductivity(self,model="Obvious",**kwargs):
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


    class Electron(unittest.TestCase):
        """

        """
        def test___init__(self,LaserPlasmaInteraction):
            self._lpi   = LaserPlasmaInteraction
            self.hot    = self.Hot(self._lpi)
            # self.cold   = self.Cold(self._lpi)

        # TODO: here general stuff about all the electrons

        class Hot(unittest.TestCase):
            """
            In UHI, super thermal electrons
            """
            def test___init__(self,LaserPlasmaInteraction):
                self._lpi = LaserPlasmaInteraction
                self.default_model={'numberTotal':'Bell1997','temperature':'Haines2009'}

            def test_numberTotal(self,model=None,**kwargs):
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
                the documentation of the LaserPlasmaInteraction unittest.TestCase.

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

            def test_lengthCaracDepth(self,model="Bell1997",**kwargs):
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

            def test_temperature(self,model="Haines2009"):
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

            def test_timeInteractionMax(self,verbose=True):
                """
                """
                return 0.

            def test_lengthInteractionMax(self,verbose=True):
                return 0.


if __name__== '__main__':
    unittest.main()
