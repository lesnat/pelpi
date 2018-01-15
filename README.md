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

## Code structure

```mermaid
graph LR
mat[Material] --> target[Target]
geom[Geometry] --> target
target[Target] --> lpi[LaserPlasmaInteraction]
laser[Laser] -->lpi[LaserPlasmaInteraction]
lpi --> pic[ParticleInCell]
```