# Package for Estimate Laser-Plasma Interaction

**WARNING: THIS IS A DEAD PROJECT !**

pelpi is an open source object-oriented python package designed to facilitate physical estimations in the context of laser plasma interaction.

It can be helpfull for obtaining good estimates to design experimental setups, or to constraint numerical parameters. It can also be used to help interpreting results from different theoretical backgrounds, or to validate simulation results with experimental scalings. 

The general approach is to declare laser and target parameters only once, and then to use theoretical models or experimental scalings to estimate the desired physical quantities. Core objective of this approach is to obtain in an easier way estimates that take several parameters, whose also needs to be estimated from laser and target fundamental properties.

Some examples/tutorials can be found in `examples/`, and a most complete documentation can be found in `docs/reference.pdf` or using `help(pelpi)`  in python interpreter.

**Note :** pelpi is actually specifically designed for ultra high intensity laser solid interaction, but also contains more general estimates and can be adapted to many other situations.

## Installation

pelpi is written for python 3 but might be compatible with 2.7.

Its only dependancies are python packages `pint` for operate with physical quantities, and `numpy` ?

### Installing

Download and extract the source code, and use the following lines at the beginning of your script

```python
import sys
pelpi_path='/path/to/pelpi/'
if pelpi_path not in sys.path:sys.path.append(pelpi_path)
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

## License

pelpi is distributed under the GPL3 license. More details can be found in `LICENSE`

## Contributing

TODO
