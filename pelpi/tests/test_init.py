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

    def test_import_warnings(self):
        import warnings

    def test_use_warnings(self):
        import warnings
        warnings.formatwarning = lambda message, category, filename, lineno, line : \
            "\n"+'%s:%s:%s\n    %s : %s' % (filename,lineno,line, category.__name__,message)+"\n"
        warnings.simplefilter('always',UserWarning)
        warnings.warn('Test Warning')

    def test_import_pelpi(self):
        import pelpi as pp


if __name__== '__main__':
    unittest.main()
