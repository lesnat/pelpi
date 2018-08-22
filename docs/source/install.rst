=======
Install
=======

pelpi is written for python 3 but might be compatible with 2.7.

Its only dependancies are python packages `pint` for operate with physical quantities, and `numpy`.

Installation
============

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


Test integrity
==============
In a python terminal, type

```python
>>> import pelpi
>>> pelpi.test()
```

Not working yet.
