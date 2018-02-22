# coding:utf8
import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)

import pelpi as pp
u=pp.unit

from examples import ExampleLPI,PelpiTest

import unittest


class test_Target(PelpiTest):
    def setUp(self):
        self.targAl = ExampleLPI().targAl

    def tearDown(self):
        del self.targAl


if __name__== '__main__':
    unittest.main()
