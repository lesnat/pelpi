#coding:utf8
from . import default_unit as _du


__all__ = ["_PelpiObject"]


class _PelpiObject(object):
    """
    Private base class for pelpi objects.
    """
    def _check_input(self,var_name,var_value,exp_type):
        """
        Check if the user input have the correct type.
        
        Compare the str conversion of exp_type with str conversion of var_value type, so exp_type can be a str.
        var_name is necessary for giving an accurate information in the Traceback.
        
        Parameters
        ----------
        var_name    : str
            Name of the variable
        var_value   : Quantity or str or ...
            User input value
        exp_type    : type or str
            Value expected type 
        
        Raises
        ------
        TypeError
            If input type is not the same as expected type.
        
        Examples
        --------
        class Laser(_PelpiObject)
            def __init__(self,wavelength,energy,time_profile,space_profile,**kwargs):
                self._check_input('wavelength'   , wavelength    , type(_du['length']))
                self._check_input('energy'       , energy        , type(_du['energy']))
                self._check_input('time_profile' , time_profile  , "<class 'pelpi.Profile.classes.Profile'>")
                self._check_input('space_profile', space_profile , "<class 'pelpi.Profile.classes.Profile'>")
                
        Notes
        -----
        This method not raise an exception if var_value is None, because this way it is possible to the user
        to not define some values that would be useless for him/her.
        
        """
        if str(type(var_value))!=str(exp_type) and (var_value is not None) :
            raise TypeError(var_name+" type is expected to be "+str(exp_type)+", but got "+str(type(var_value))+" instead.")

    def _initialize_defaults(self,input_dict=None):
        """
        Initialize `default` dictionary.
        
        This dict is used for saving user input values, and to give the user the
        choice of a default value returned by the desired method.
        This way, the user can choose a value for, let say temperature for all the following
        instructions.
        It also allows to change some object input properties easily, with no need
        to instanciate a new object each time.
        
        This method first create an empty dict, then get all the class methods
        and initialize their default value to None. Finally it creates entries for input values.
        This last might be done after initializing class method default 
        because this way the new value erase the None value defined previously
        (there might always be a method that return input parameters).

        Parameters
        ----------
        input_dict : dict
            {var_name, var_value}
            var_name : str
                Name of the input variable
            var_value : Quantity or object or ...
                Value of the input variable
        """
        #self._check_input()
        
        # Create the dictionnary
        self.default={}
        
        
        # Loop over all class attributes
        for attr_name in dir(self):
            # Get the 'attr_name' type
            attr_type = type(getattr(self,attr_name))
            # if 'attr_name' is a method, and is not private (i.e. not starts with '_')
            if str(attr_type)=="<type 'instancemethod'>" and attr_name[0]!="_":
                # then a new dict entry is initialize to None
                self.default[attr_name]=None
        
        # Put input_dict into default if input_dict is defined.
        # This might be done after creating all the `attr_name`s entries. This way it replaces None value.
        if input_dict is not None:
            for key,val in input_dict.items():
                self.default[key]=val
        
        
    def _estimate(self,lpi,model_name,method_name,**kwargs):
        """
        Return the result of lpi.model.model_name.method_name(**kwargs)
        
        """
        # Check developer input type. kwargs types are tested in model methods.
        self._check_input('lpi'         , lpi           , "<class 'pelpi.LaserPlasmaInteraction.classes.LaserPlasmaInteraction'>")
        self._check_input('model_name'  , model_name    , str)
        self._check_input('method_name' , method_name   , str)
        
        # Find the 'model_name' class in lpi.model
        model_class = getattr(lpi.model , model_name)
        # and instanciate is with the lpi instance
        model_inst  = model_class(lpi)
        # When this is done, get the 'method_name' method from the 'model_name' instance
        method      = getattr(model_inst, method_name)
        # and get the result of 'method_name' when using it with kwargs
        res         = method(**kwargs)
        # Finally return the result
        return res



