#Package for Estimate Laser-Plasma Interaction (pelpi)

pelpi core functionality -> lpi ; + calculus for pic or laser

tatata, designed for ...

```python
# TODO : 
import numpy as np
import matplotlib.pyplot as plt
import pelpi as pp

u		= pp.unit # get the pint unitRegistry instance

# Profile as a function (then all @staticmethod)
sprof	= pp.Profile.gaussianIsotrope2D(fwhm=10 * u('um'))
print("2D integrate of laser profile : {}".format(pp.Profile.integral2D(sprof)))
# OR Profile as an object
sprof	= pp.Profile('gaussianIsotrope2D',fwhm=10 * u('um'))
print("2D integrate of laser profile : {}".format(sprof.integral2D()))

def tprofile(t): # problem for getting I0 ? 
    			 # at 0 or max(prof(range(-carac length,carac length)))
    constrast = 1e-8 * u('') # dimensionless
    t0 = 1 * u('ps')
    if t<-t0 or t>t0: # centered in 0.
        return contrast 
   	else:
        return pp.Profile.gaussian1D(fwhm=30 * u('fs')) # maximum = 1

tprof	= pp.Profile.user1D(tprofile) # tprof is object or function ? arg Carac length ?
tprof.plot()

# Define chirp profile ?
laser	= pp.Laser(
    wavelength		= 0.8 * u('um'),
    energy			= 2.0 * u('J'),
    
	space_profile	= sprof, # profile or envelope ?
    time_profile	= tprof,
    time_chirp		= 1. * u('') # kwarg, dimensionless constant function
    time_phase		= np.pi/4 * u('rad') # kwarg, phase in sin(time_chirp*wt+phi)
)

sprof	= pp.Profile('gaussianIsotrope2D',fwhm=12 * u('um'))
print("2D integrate of laser profile : {}".format(sprof.integral2D()))

laser.set('space_profile',sprof)

prof	= pp.Profile('constant1D',x0=15 * u('um'),x1=25 * u('um'))
mat		= pp.Target.database.Al
# OR
mat 	= pp.Material.search("Al")
target	= pp.Target(mat,prof)

lpi 	= pp.LaserPlasmaInteraction(laser,target)

ekin	= np.linspace(0.1,20,100) * u('MeV')
plt.figure()
help(lpi.electron.hot.temperature)
for model in ["Beg1997","Haines2009","Wilks1992"]:
    Teh=lpi.electron.hot.temperature(model)
    MB=lpi.model.Common.distribution('MB',kinetic_energy=ekin,temperature=Teh)
    # or lpi.Common.distribution ?
    plt.plot(ekin,MB,label=model)

pic 	= pp.ParticleInCell(lpi)

print("Simulation length : {}".format(pic.length_simulation()))
# pic.set(display=True)
pic.set('length_simulation',64 * u('um'))
print("Simulation times : {}".format(pic.time_simulation()))

pic.autoconvert_to_code_units('all')
print("Simulation times : {}".format(pic.time_simulation()))
```



## v0.1

### general

in init & general structure

#### Properties

import, prefered_unit

#### TODO

warnings?

structure OK ?

start estimate methods by e like electron.hot.e_density for ex. for differenciate estimates from exact calculations ? analytical calc. also comes from models.

### _PelpiObject

Base class for all other objects

#### Properties

_checkInput, _set ('input':True ??),

electron.hot etc ?

how to : _addMethod

#### TODO

_defineMethodFromArg

checkHypotheses ?



### Profile

Define basics profiles

#### Properties

Integrates

#### TODO

user-defined



### Laser

Define basic laser properties

#### Properties

intensity, intensityPeak, nc

#### TODO

polarisation, constrast, plot



### Target

Define basic target properties

#### Properties

ne, ni (electron.density ?)

#### TODO

Geometry, database



### LaserPlasmaInteraction

Instanciate a LaserPlasmaInteraction object (add)

#### Properties

plasma : calculation of plasma parameters : OK

electron.hot.method : access to models : OK with _Estimate (see models structure)

target.method : basic target properties + estimations (via _addMethod) : KO

#### TODO

More models



### ParticleInCell

PIC estimates

#### Properties

dx, CU calculations, Tsim, Lsim, Npatches (KO)

#### TODO

change struct for $\neq$ codes ?

autoconvert to CU



## TODO

Defining class attributes model_HotElectronTotalNumber or subclass model.HotElectronTotalNumber ? or this + kwargs in methods for giving the choice to the user ?

examples on how to use pelpi in different ways (using models, using lpi methods with/wo kwargs)

remove all class attributes ?

split getInfo into different precise functions or print when call a method if verbosities=0.

Model accesibility via pelpi.Model wo having a Model mother class

split models into different files ?

function for displaying quantities

replace .to_base_units() by .to('dimensionless') for dimensionless units (more explicit)

hotElectronTotalNumber or totalNumberHotElectron or numberTotalHotElectron ? hotElectronTemperature or temperatureHotElectron ? hotElectronPenetrationDepth or hotElectronStoppingLength or lengthStoppingHotElectron ? (dimension + dimension adjective + particle adjective + particle **OR** particle adjective + particle (or Laser/Target ...) + dimension + dimension adjective)

a0 or a0/2 in Wilks1992 model ?

argument loop=True -> loop over all the models with a checkHypotheses and try, except for getting the max value for ex. (func=max in arguments and return func(list))

make a difference between warnings with and wo a test  in checkHypotheses?

hide attributes + add corresponding method + add a set(variable) method for reset an input variable value

Profile class for both laser & target ? Base profiles (1d/2d) + user func.

Create 1 private variable for each method for using the set method **OR** argument=None and if None use method -> need to define intermediate variables in methods. Easy to implement but can be heavy if want to do many calculus with a user-defined Lsim for ex. Or options + dictionnary with defaults

```python
self._userValues={\
                'resx':False,\
 				'resy':False,\
            	'Lsim':False,\
				'Tsim':False\
                }

self._defaultValues={}

# class.set('resx',20) 
# -> 	class._userValues['resx']=True
# 		if not class._defaultValues['resx'] : class._defaultValues.append('resx':20)

def Tsim(self):
    if self._userValues['Lsim']:
        Lsim=self._default['Lsim']
    else:
        Lsim=self.length_simulation()
        
    return (Lsim/_u.c).to(_pu['length'])
```



## Code structure

```mermaid
graph TB
mat[Material] ==> target[Target]
geom[Geometry] ==> target
target[Target] ==> lpi[LaserPlasmaInteraction]
profile[Profile] ==> laser[Laser]
laser ==>lpi[LaserPlasmaInteraction]

lpi ==> pic[ParticleInCell]

input{user input} -x laser
input -x mat
input -x geom
input -x profile
```

## Estimations

```mermaid
graph LR
lpi[LaserPlasmaInteraction] --> plasma[PlasmaParameters]
lpi --> laser[Laser]
lpi --> target[Target]
lpi --> electron[Electron]
electron --> hot[Hot]
electron --> cold[Cold]
lpi --> ion[Ion]
lpi --> photon[Photon]
lpi --> positron[Positron]


hot -x outHot(Temperature, Energy cutoff, ...)
cold -x outCold(...)
ion -x outIon(Energy cutoff, ...)
photon -x outPhoton(...)
positron -x outPositron(...)
plasma -x outPlasma(Debye length, ...)
laser -x outLaser(Absorption efficiency, ...)
target -x outTarget(Spitzer conductivity, ...)
```

