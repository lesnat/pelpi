#coding:utf8
from . import prefered_unit as _pu


__all__ = ["_Estimate"]


class _PelpiObject(object):
    """
    Private base class for pelpi objects.

    It contains methods such as _ckeckInput and set,
    and automatically create methods for acessing to input param ?
    """
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

    def _set(self,variable_name,value):
        """
        Reset an input parameter to a new value.

        Parameters
        ----------
        variable_name : str
            Name of the variable to reset a new value.
        value : variable type
            New value of the variable.

        Examples
        --------
        Assuming a ``pelpi.Laser`` is instanciated as ``las``

        >>> las.set(wavelength,1.054 * pelpi.unit('um'))
        >>> las.wavelength()
        <Quantity(1.054,'um')>

        The 'set' method can be ... what is the name ?

        >>> las.set(wavelength,1.054*pelpi.unit('um')).set(energy,2*pelpi.unit('J'))

        Notes
        -----
        Because all the informations are accessed only in methods
        and the class attributes are private ; all the following calculations
        would be performed with the new wavelength value without having to instanciate
        a new ``pelpi.Laser`` object, or setting the attribute to a new value manually.
        """
        self._checkInput(variable_dictionnary={variable_name:type(value)})
        variable = self.__dict__.get("_"+variable_name)
        variable = value
        return self

    def _defineMethodsFromVariables(self): # TODO : _setAttributes() & _setMethods
        """
        Define methods for accessing to user input
        without having an access to the class attributes.
        It is then safer and have a more coherent notation.
        """
        # method.__doc__="Returns\n------\n"+variable_name+" : "+str(type(value))
        # self.__dict__.get()
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
