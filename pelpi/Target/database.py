#coding:utf8

from .._global import _u
from .classes import _UserMaterial

class _MaterialDatabase(object):
    Al=_UserMaterial{
        'density'       : 2.69890e3 * _u('kg/m**3'),
        'atomic_mass'   : 26.98154 * _u('amu'),
        'Z'             : 13 * _u(''),
    }

    W=_UserMaterial{
        'density'       : 1.93000e4 * _u('kg/m**3'),
        'atomic_mass'   : 183.85 * _u('u'),
        'Z'             : 74 * _u(''),
    }

    # CH={
    #     'density'       :
    # }
