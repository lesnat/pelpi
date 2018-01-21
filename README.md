#Package for Estimate Laser-Plasma Interaction (pelpi)

pelpi core functionality -> lpi ; + calculus for pic or laser

tatata, designed for ...



## TODO

global variables (in a separate file ?)

checkHypotheses method

remove "get" in method name ?

change of keyword arguments in methods : HotElectronTotalNumber(model="Bell1997",Teh= ... + default) for allowing user-defined arguments (wo defining set--- methods)

Defining set--- methods for the interaction of different files ?

Defining class attributes model_HotElectronTotalNumber or subclass model.HotElectronTotalNumber ? or this + kwargs in methods for giving the choice to the user ?

examples on how to use pelpi in different ways (using models, using lpi methods with/wo kwargs)

add "@author" in models doc

remove all class attributes ?

split getInfo into different precise functions or print when call a method if verbosities=0.

How to have only one unit registry

Model accesibility via pelpi.Model wo having a Model mother class

split models into different files ?

density + number density in prefered_unit

function for displaying quantities

replace .to_base_units() by .to('dimensionless') for dimensionless units (more explicit)

hotElectronTotalNumber or totalNumberHotElectron or numberTotalHotElectron ? hotElectronTemperature or temperatureHotElectron ? hotElectronPenetrationDepth or hotElectronStoppingLength or lengthStoppingHotElectron ? (dimension + dimension adjective + particle adjective + particle **OR** particle adjective + particle (or Laser/Target ...) + dimension + dimension adjective)

Possible optimisation of memory usage with modifying self._lpi in lpi subclasses ? (global variable "lpi")

Give default behaviour to models or not ? default behaviour do not force the user to understand the models

a0 or a0/2 in Wilks1992 model ?

argument loop=True -> loop over all the models with a checkHypotheses and try, except for getting the max value for ex. (func=max in arguments and return func(list))

make a difference between warnings with and wo a test  in checkHypotheses?

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

