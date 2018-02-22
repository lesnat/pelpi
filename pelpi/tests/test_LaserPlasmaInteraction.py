# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

from examples import ExampleLPI,PelpiTest

import pelpi as pp
u=pp.unit

import unittest


class test_LaserPlasmaInteraction(PelpiTest):
    def setUp(self):
        self.lpiGGAl = ExampleLPI().lpiGGAl

    def tearDown(self):
        del self.lpiGGAl



if __name__== '__main__':
    unittest.main()
