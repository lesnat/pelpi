import sys
Modules_path="../../"
if sys.path[0]!=Modules_path:sys.path.insert(0, Modules_path)
import unittest

class test_Import(unittest.TestCase):
    def test_import_pint(self):
        import pint

    def test_define_unit(self):
        import pint
        unit=pint.UnitRegistry()

    def test_import_pelpi(self):
        import pelpi as pp
        
    def test_examples(self)
        from .examples import ExampleLPI


if __name__== '__main__':
    unittest.main()
