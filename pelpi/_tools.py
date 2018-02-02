#coding:utf8
from . import prefered_unit as _pu


__all__ = ["_Estimate"]


class _PelpiObject(object):
    """
    Private base class for pelpi objects.

    It contains methods such as _ckeckInput and set,
    and automatically create methods for acessing to input param ?
    """

    def __init__(self):
        pass

    def _initialize_defaults(self,var_dict):
        self._user_values={}
        self._setInputToDict(var_dict)
        self._setMethodsToDict()
        self._setInputToMethod(var_dict)


    def _setInputToDict(self,var_dict):
        """
        Set the object __init__ parameters to _user_values dictionary.
        """
        for key,val in var_dict.items():
            self.set_default(key,val)

    def _setMethodsToDict(self):
        """
        Initialize all the object method names to None in _user_defined dict.
        """
        exclude=['set_default','get_default'] # + model, plasma, database etc ?
        for method in dir(self):
            if method[0]!='_' and method not in exclude: # If public method
                self.set_default(method,None)
                # getattr(self,method).__doc__=\
                # "Return\n------\nThe input parameter "+method# not working

    def _setInputToMethod(self,var_dict):
        """
        Define methods for accessing the input values (now in dict)
        """
        for key in var_dict.keys():
            self.__dict__[key] = \
                lambda : self.get_default(key=key)

    # def _initialize_defaults(self,var_dict):
    #     self._setInputToDict(var_dict)
    #     self._setMethodsToDict()
    #     self._setInputToMethod(var_dict)


    def _dor(self,result,**kwargs):
        """
        Return default or result (udom).

        Check if a default value for result is defined,
        if yes return it
        else return method result with the same name.

        Default values are prior to non-default.
        """
        # func_name=
        return result
        if self.get_default(result)!=None:
            return self.get_default(result)
        else:
            return result

    # def _udom(self,variable_name,**kwargs):
    #     """
    #     Use default or method (udom).
    #
    #     Check if a default value for variable_name is defined,
    #     if yes return it
    #     else return method result with the same name.
    #
    #     Default values are prior to non-default.
    #     """
    #     if self.get_default(variable_name)!=None:
    #         return self.get_default(variable_name)
    #     else:
    #         return getattr(self.__dict__,variable_name)(**kwargs)

    def _checkInput(self,variable_dictionnary):
        """
        Dictionary of variables with expected type.

        Examples
        --------
        >>> class Laser(_PelpiObject):
        ...     def __init__(self,*args):
        ...     # Some instructions here
        ...     variable_dictionnary={'wavelength':'Quantity<>','energy':'Quantity<>','Profile':"<class 'pelpi.Profile'"}
        ...     self._checkInput(variable_dictionnary)

        Raises
        ------
        TypeError

        NameError (if input not in variable_dictionnary.keys())

        Notes
        -----
        If the variable type is NoneType, no exception is raised.
        """
        pass

    def set_default(self,key,value):
        """
        Set a parameter to a default value.
        This can be an input parameter or not.

        Parameters
        ----------
        key : str
            Name of the variable to set.
        value : object, quantity, str, ...
            New value of the variable.

        Examples
        --------
        Assuming a ``pelpi.LaserPlasmaInteraction`` is instanciated as ``lpi``

        You can use the set method for setting a new value to
        an input parameter

        >>> lpi.laser.wavelength()
        <Quantity(0.8,'um')>

        >>> lpi.laser.set('wavelength',1.054 * pelpi.unit('um'))
        >>> lpi.laser.wavelength()
        <Quantity(1.054,'um')>

        Then all the further calculations are done with this new value.


        You can also use it for setting a calculated parameter to a new value

        >>> lpi.electron.hot.set('temperature',1*pelpi.unit('MeV'))

        You can still access to estimates

        >>> lpi.electron.hot.temperature(model="Haines2009")
        <Quantity(0.72,'MeV')>

        But hot electron temperature have now a default behaviour

        >>> lpi.electron.hot.temperature()
        <Quantity(1.0,'MeV')>

        And further estimates can be acomplished with both of them

        >>> pic=pp.ParticleInCell(lpi)

        Without default temperature

        >>> Teh = lpi.electron.hot.temperature(model="Haines2009")
        >>> pic.length_cell(temperature=Teh)
        <Quantity(0.1456847,'um')>

        Or with

        >>> pic.length_cell()
        <Quantity(0.125468,'um')>

        This can be usefull when a lot of estimates
        are done with the same parameters, or when a rough estimate or exp. values
        can be set.

        Notes
        -----
        >>> lpi.electron.set_default('temperature',value) would not work.
        -> needs to define to more close of the method.
        """
        self._user_values[key]=value

    def get_default(self,key='all'):
        """
        Return the default values.

        For all values variable_name='all'

        """
        if key=='all':
            return self._user_values
        else:
            return self._user_values[key]


class _Laser(_PelpiObject):
    pass

class _Target(_PelpiObject):
    pass

class _Electron(_PelpiObject):
    def __init__(self):
        self.hot=self._Hot()

    class _Hot(_PelpiObject):
        pass

    class _Cold(_PelpiObject):
        pass

class _Ion(_PelpiObject):
    pass

class _Photon(_PelpiObject):
    pass

class _Positron(_PelpiObject):
    pass


class _Estimate(_PelpiObject):
    """
    Class for using estimations models.

    It takes strings as arguments (model_name, method_name) and return the result
    of the given method.
    It is recommended to use this class in all estimations methods of
    LaserPlasmaInteraction.

    Parameters
    ---------
    LaserPlasmaInteraction, object
        Instanciated class of LaserPlasmaInteraction
    model_name, string
        Needed model name
    available_models, list of strings
        List of all models that can be used with the lpi method

    Methods
    ------
    use
        Return the result of the model choosen method
    """
    def __init__(self,LaserPlasmaInteraction,model_name,available_models):
        if str(type(LaserPlasmaInteraction))!="<class 'pelpi.LaserPlasmaInteraction.classes.LaserPlasmaInteraction'>":
            raise TypeError("'LaserPlasmaInteraction' type must be a pelpi module, but it is "+str(type(LaserPlasmaInteraction)))
        if type(model_name)!=str:
            raise TypeError("'model_name' type must be 'string', but it is "+str(type(model_name)))
        if type(available_models)!=list:
            raise TypeError("'available_models' type must be 'list', but it is "+str(type(available_models)))

        # TODO: Replace by _checkInput method

        self._lpi       = LaserPlasmaInteraction
        if model_name in available_models:
            # Get the 'model_name' class from the 'model' attribute of _lpi
            Model=getattr(self._lpi.model,model_name)
            # and instanciate it with _lpi
            self.model=Model(self._lpi)
        else:
            raise NameError("Model name "+model_name+" not found. Available models are "+str(available_models))

    def use(self,method_name,dim,*args):
        """
        Return the result of the model choosen method.

        Result is automatically converted into the pelpi.prefered_unit unit.

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

        if dim not in _pu.keys():
            raise NameError("'dim' name "+dim+" not found. Available dimensions are "+str(_pu.keys()))

        # Get the method from the model
        Method = getattr(self.model,method_name)
        # Use it with kwargs and convert it
        return Method(*args).to(_pu[dim]) # TODO: check if OK with args

class _Model(_PelpiObject):
    """
    Base class for models.
    """
    def __init__(self):
        # self.electron = electron
        pass

    def _addMethod(self):
        pass

# def _addMethod(InObject,OutObject,method):
#     OutObject.__dict__.get(method) = InObject.__dict__.get(method)
