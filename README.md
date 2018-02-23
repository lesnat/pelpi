# Package for Estimate Laser-Plasma Interaction

pelpi is an open source object-oriented python package designed to facilitate physical estimations in the context of laser plasma interaction.

It can be helpfull for obtaining good estimates to design experimental setups, or to constraint numerical parameters. It can also be used to help interpreting results from different theoretical backgrounds, or to validate simulation results with experimental scalings. 

The general approach is to declare laser and target parameters only once, and then to use theoretical models or experimental scalings to estimate the desired physical quantities. Core objective of this approach is to obtain in an easier way estimates that take several parameters, whose also needs to be estimated from laser and target fundamental properties.

A more complete documentation can be found at [...]() or in `docs/reference.pdf`.

**Note :** pelpi is actually specifically designed for ultra high intensity laser solid interaction, but also contains more general estimates and can be adapted to many other situations.

## Basic examples

Assuming you work with a UHI laser interacting with a solid target

### Get electron number density

```python
pelpi
```



### Estimate hot electron energy cutoff

, that are respectively declared as `laser` and `target` pelpi objects ; you can estimate number of hot electron from the Bell model as follows

```python
lpi=pelpi.LaserPlasmaInteraction(laser,target)


```

### Estimate minimal PIC space resolution

If you work with particle-in-cell codes, you might need to do some calculations several times to check if neutrality or CFL is OK for example. Those estimates often needs physical estimations, such as energy cutoff or temperature, and some can be calculated as follows

```python

```





## Installation

pelpi is written in python 3 but might be compatible with 2.7.

Its only dependancies are python packages `pint` for operate with physical quantities, and `numpy` ?

### Installing

via pip

```bash
pip3 install pelpi
```

via git

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

If an error occured, please contact me.



## Licence



## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.
