.. pelpi documentation master file, created by
   sphinx-quickstart on Sat Jan 20 17:40:19 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*****
pelpi
*****

pelpi is an open source object-oriented python package designed to facilitate
physical estimations in the context of laser plasma interaction.

It can be helpfull for obtaining good estimates to design experimental setups,
or to constraint numerical parameters.
It can also be used to help interpreting results from different theoretical
backgrounds, or to validate simulation results with experimental scalings.

The general approach is to declare laser and target parameters only once,
and then to use theoretical models or experimental scalings to estimate
the desired physical quantities. Core objective of this approach is to obtain
in an easier way estimates that take several parameters, whose also needs
to be estimated from laser and target fundamental properties.

.. toctree::
   :maxdepth: 3

   intro
   install
   use
   examples
