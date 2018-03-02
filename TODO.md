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

import, default_unit

#### TODO

start estimate methods by e like electron.hot.e_density for ex. for differenciate estimates from exact calculations ? analytical calc. also comes from models.

function for displaying quantities

### _PelpiObject

Base class for all other objects

#### Properties

_checkInput, _set ('input':True ??),

electron.hot etc ?

how to : _addMethod

#### TODO

_defineMethodFromArg

checkHypotheses ?

split _input & _default ?



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

a0 or a0/2 in Wilks1992 model ?



### ParticleInCell

PIC estimates

#### Properties

dx, CU calculations, Tsim, Lsim, Npatches (KO)

#### TODO

change struct for $\neq$ codes ?

autoconvert to CU
