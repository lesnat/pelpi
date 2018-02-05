#coding:utf8

from .._global import _u

class _MaterialDatabase(object):
    _base={
        'density'       : 1 * _u('kg/m**3'),
        'atomic_mass'   : 1 * _u('amu'),
        'Z'             : 1 * _u(''),
        'A'             : 1 * _u(''),
    }


    Al={
        'density'       : 2.69890e3 * _u('kg/m**3'),
        'atomic_mass'   : 26.98154 * _u('amu'),
        'Z'             : 13 * _u(''),
        'A'             : 27 * _u(''),
    }

    W={
        'density'       : 1.93000e4 * _u('kg/m**3'),
        'atomic_mass'   : 183.85 * _u('u'),
        'Z'             : 74 * _u(''),
        'A'             : 184 * _u(''),
    }

    # CH={
    #     'density'       :
    # }
