#coding:utf8
from . import default_unit as _du


__all__ = ["_PelpiObject","_Estimate"]


class _PelpiObject(object):
    """
    Private base class for pelpi objects.
    """
    def _check_input(self,input_lst):
        """
        Compare conversion into str
        
        Parameters
        ----------
        lst : list of tuples
            {(name, value, type)}
            name    : str
            value   : Quantity, object, ...
            type    : type or str, value expected type 
        
        Raises
        ------
        NameError
            If input not in in_ref_dict.keys()
        TypeError
            If input type is not ref
        
        Examples
        --------
        class Laser(_PelpiObject)
            def __init__(self,wavelength,energy,time_profile,space_profile,**kwargs):
                input_lst = [\
                ('wavelength'   , wavelength    , type(_du['length'])),\
                ('energy'       , energy        , type(_du['energy'])),\
                ('time_profile' , time_profile  , 'pelpi.Profile.classes.Profile'),\
                ('space_profile', space_profile , 'pelpi.Profile.classes.Profile')\
                ]
                
                self._check_input(input_lst)
        """
        for name,value,type_ in input_lst:
            if str(type(value))!=str(type_):
                raise TypeError(name+" type is expected to be "+str(type_)+" but it is "+str(type(value)))
        

class _Estimate(_PelpiObject):
    """
    Class for using estimations models.

    It takes strings as arguments (model_name, method_name) and return the result
    of the given method.
    It is recommended to use this class in all estimations methods of
    LaserPlasmaInteraction.

    Parameters
    ----------
    LaserPlasmaInteraction, object
        Instanciated class of LaserPlasmaInteraction
    model_name, string
        Needed model name
    available_models, list of strings
        List of all models that can be used with the lpi method

    Methods
    -------
    use
        Return the result of the model choosen method
    """
    def __init__(self,LaserPlasmaInteraction,model_name,available_models):
        self._lpi       = LaserPlasmaInteraction
        if model_name in available_models:
            # Get the 'model_name' class from the 'model' attribute of _lpi
            Model=getattr(self._lpi.model,model_name)
            # and instanciate it with _lpi
            self.model=Model(self._lpi)
        else:
            raise NameError("Model name "+model_name+" not found. Available models are "+str(available_models))

    def use(self,method_name,dim,**kwargs):
        """
        Return the result of the model choosen method.

        Result is automatically converted into the pelpi.default_unit unit.

        Parameters
        ---------
        method_name, string
            Needed method name of the model
        dim, string
            Dimension of the result (i.e. 'temperature', 'conductivity', ...)
        args
            Arguments to use in the method
        """
        if type(method_name)!=str:
            raise TypeError("'method_name' type must be 'string', but it is "+str(type(method_name)))
        if type(dim)!=str:
            raise TypeError("'dim' type must be 'string', but it is "+str(type(dim)))

        if dim not in _du.keys():
            raise NameError("'dim' name "+dim+" not found. Available dimensions are "+str(_du.keys()))

        # Get the method from the model
        Method = getattr(self.model,method_name)
        # Use it with kwargs and convert it
        return Method(**kwargs).to(_du[dim]) # TODO: check if OK with args


