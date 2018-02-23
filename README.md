# Package for Estimate Laser-Plasma Interaction

pelpi is an open source object-oriented python package designed to facilitate physical estimations in the context of laser plasma interaction.

It can be helpfull for obtaining good estimates to design experimental setups, or to constraint numerical parameters. It can also be used to help interpreting results from different theoretical backgrounds, or to validate simulation results with experimental scalings. 

The general approach is to declare laser and target parameters only once, and then to use theoretical models or experimental scalings to estimate the desired physical quantities. Core objective of this approach is to obtain in an easier way estimates that take several parameters, whose also needs to be estimated from laser and target fundamental properties.

A documentation can be found in `docs/reference.pdf` or using `help(pelpi)`  in python interpreter.

**Note :** pelpi is actually specifically designed for ultra high intensity laser solid interaction, but also contains more general estimates and can be adapted to many other situations.

## Basic examples

Assuming you work with a UHI laser interacting with a solid target.

### Get electron number density

You can initialize a pelpi estimations script and print the electron number density (number per unit of volume) as follows. This example shows how to instanciate pelpi objects and to get calculation results.

```python
# Import pelpi
import pelpi as pp
# Instanciate a Material object
Al = pp.Material(
	density		= 2.7e3 * pp.unit('kg/m**3'),	# define value and unit (with pint)
    atomic_mass = 27.0 * pp.unit('amu'),		# atomic mass unit
    Z			= 13 * pp.unit('')				# dimensionless
)
# Get electron number density
ne = Al.electron.number_density()
# and print it
print("ne = {:.5E}".format(ne))
```

### Estimate super-thermal electron energy cutoff

Assuming a `Laser` and `Target` pelpi objects are respectively instanciated as `laser` and `target` ; you can estimate the energy cutoff of super-thermal electrons from the Malka model as follows. Details of the models can be found in specific methods. This example shows how to get simple or complex estimates from a `LaserPlasmaInteraction` instance.

```python
# Instanciate a LaserPlasmaInteraction object
lpi = pp.LaserPlasmaInteraction(laser,target)
# Get an estimate of super-thermal (hot) electron temperature from Beg's model
Teh = lpi.electron.hot.temperature(model="Beg1997")
# and use it in a more complex model to get hot electron energy cutoff
E_cutoff = lpi.electron.hot.energy_cutoff(model="Malka2001",temperature=Teh)
```

Malka model is not implemented yet but this example might work soon.

### Estimate PIC cell length

If you work with Particle-In-Cell codes, you might need to do some calculations several times to check that some numerical conditions are respected. Those estimates often needs physical estimations, such as energy cutoff or temperature. This example shows how to change default unit conversion (via the `pint` package), and to use `default` dictionnary to set a default behaviour for further estimates.

```python
# Instanciate a ParticleInCell object from your LaserPlasmaInteraction instance
pic = pp.ParticleInCell(lpi)
# Change length default unit to micrometer
pp.default_unit['length'] = pp.unit('um')
# Estimate maximal acceptable cell length, considering only the target properties
dx = pic.length_cell('target',temperature=Teh)
# You can now set a default value for dx
pic.default['length_cell'] = 0.01 * pp.unit('um')
# and get other results with this default behaviour
dt = pic.time_step('target',CFL=True,temperature=Teh)
```

You can find more complete examples in `examples/`.

## General structure

Only few objects are necessary to perform a full set of estimates. The interaction between all existing classes are represented next, where bold arrows means that instance might be given as a parameter, when doted arrows means `pint Quantity` input (using `pelpi.unit`).

```mermaid
graph LR
mat[Material] ==> target[Target]
target[Target] ==> lpi[LaserPlasmaInteraction]
profile[Profile] ==> laser[Laser]
laser ==>lpi[LaserPlasmaInteraction]

lpi ==> pic[ParticleInCell]

input{user input} -x laser
input -x mat
input -x profile
```

All the estimates and object properties are accessible only from methods ; this way if you re-define an input parameter then all the further calculations are automatically done with its new value. Input parameters are stored in `default` dictionnary and might only be accessed via correspondant method.

Discovering available methods is possible by running one of `examples/` scripts in interactive python console, and use auto-completion to look on object attributes. A complete documentation will be available soon.

## Installation

pelpi is written for python 3 but might be compatible with 2.7.

Its only dependancies are python packages `pint` for operate with physical quantities, and `numpy` ?

### Installing

Download and extract the source code, and use the following lines at the beginning of your script

```python
import sys
pelpi_path='/path/to/pelpi/'
if sys.path[0]!=pelpi_path:sys.path.insert(0,pelpi_path)
import pelpi
```

**TODO**: via pip (not working yet)

```bash
pip3 install pelpi
```

**TODO**: via git (`setup.py` not present yet)

```bash
git clone ...
cd pelpi
./setup.py
```

### Test integrity

In a python terminal, type

```python
>>> import pelpi
>>> pelpi.test()
```

Not working yet.

## Licence

TODO

## Contributing

TODO
