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
        >>> class Laser(_PelpiObject)
        >>>     def __init__(self,wavelength,energy,time_profile,space_profile,**kwargs):
        >>>         self._check_input('wavelength'   , wavelength    , type(_du['length']))
        >>>         self._check_input('energy'       , energy        , type(_du['energy']))
        >>>         self._check_input('time_profile' , time_profile  , "<class 'pelpi.Profile.classes.Profile'>")
        >>>         self._check_input('space_profile', space_profile , "<class 'pelpi.Profile.classes.Profile'>")
                
        Notes
        -----
        This method do not raise an exception if var_value is None, because this way it is possible to the user
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
        self._default={}
        
        
        # Loop over all class attributes
        for attr_name in dir(self):
            # Get the 'attr_name' type
            attr_type = type(getattr(self,attr_name))
            # if 'attr_name' is a method, and is not private (i.e. not starts with '_')
            if str(attr_type)=="<type 'instancemethod'>" and attr_name[0]!="_":
                # then a new dict entry is initialize to None
                if attr_name!='set' and attr_name!='get':
                    self.set(attr_name,None,verbose=False)
        
        # Put input_dict into default if input_dict is defined.
        # This might be done after creating all the `attr_name`s entries. This way it replaces None value.
        if input_dict is not None:
            for key,val in input_dict.items():
                self.set(key,val,verbose=False)
        
    def set(self,key,value,verbose=True):
      """
      Set default values.
      
      Parameters
      ----------
      key : str
        Name of the default entry. It could be input object parameter or object instance method
      value : Quantity or str or ...
        New value of the default entry
      verbose : bool, optional
        If True, the ``set`` method will print warning and sucess messages. Otherwise it does not print anything
      """
      if verbose and (key not in self._default.keys()):
        # self._warns(..) ?
        print("WARNING : key `%s` not present in default dictionnary. Creating a new entry ..."%key)
      
      self._default[key]=value
      
      if verbose:
        print("Default entry for variable `%s` was succesfully set to value `%s`"%(key,value))
        
        
    def get(self,key="all"):
      """
      Returns
      -------
      Default value of the entry `name`
      
      Parameters
      ----------
      name : str, optional
        Entry name to get
        
      Notes
      -----
      If `name` is set to "all", the ``get`` method will return the whole default dictionnary
      """
      if key=="all":
        return self._default
      elif key in self._default.keys():
        return self._default[key]
      else:
        raise KeyError("Default entry `%s` does not exist."%key)
        
        
    def _default_or_result(self,key,result,dimension=None):
      """
      Returns
      -------
      Default value if it is not None, result otherwise.
      
      Parameters
      ----------
      key : str
        Name of the current method, for accessing default value.
      result : Quantity or ...
        Value of the result
      dimension : str
        Dimension of the result. Might be a key of the default_unit dictionary or None (for str for example)
      """
      d = self.get(key)
      if d is not None:
        return d
      elif dimension is not None:
        return result.to(_du[dimension])
      else:
        return result
      
    def _estimate(self,root_inst,model_name,method_name,**kwargs):
        """
        Returns
        -------
        Result of root_inst.model.model_name.method_name(**kwargs)
        
        Parameters
        ----------
        root_inst : object
            Instance of pelpi root object where the estimate need to be performed. Typically a LaserPlasmaInteraction instance
        model_name : str
            Name of the model to use
        method_name : str
            Name of the method of the model to use. It should contains all the 'path' from model_name to the method
        **kwargs
            Keywords arguments to use in the method
            
        Examples
        --------
        Assuming you are defining the 'temperature' method in electron.hot LaserPlasmaInteraction sub-class
        
        >>> def temperature(self,model,**kwargs):
        >>>     if self.default['temperature'] is not None: # If a default value exists
        >>>         return self.default['temperature']      # Return default value
        >>>     else:
        >>>         temperature = self._estimate(self._lpi,model,'electron.hot.temperature',**kwargs) # Else get the estimate
        >>>         return temperature.to(_du['temperature'])   # And return the result, converted to default units.
        """
        # Check developer input type. kwargs types are tested in model methods.
        self._check_input('model_name'  , model_name    , str)
        self._check_input('method_name' , method_name   , str)
        
        ### Get an instance of 'model_name'
        # Find the 'model_name' class in root_inst.model
        model_class = getattr(root_inst.model , model_name)
        # and instanciate is with the 'root_inst' instance
        model_inst  = model_class(root_inst)
        
        ### Get the 'method_name' method from 'model_inst' instance
        # Initialize the iterator 'attr' ; it should point the model instance
        attr=model_inst
        # Loop over 'method_name' sub-objects (splited by the '.' character)
        for sub_object in method_name.split('.'):
            # The iterator go deeper and deeper in the 'model_name' attributes, untill it reaches the last 'method_name' sub-object
            attr      = getattr(attr, sub_object)
        # The iterator now point to the last 'method_name' sub-object, that is the desired method
        method = attr
        # Explanations :
        # Because getattr can not get imbricated attributes in one time,
        # it is necessary to loop over imbricated attributes.
        # Example : 
        # assuming method_name = 'electron.hot.temperature' and model_name='ExampleModel'
        # Before the loop, the iterator 'attr' should point to ExampleModel instance
        # then it would point to :
        #   ExampleModel.electron
        #   ExampleModel.electron.hot
        #   ExampleModel.electron.hot.temperature
        # so after looping over all attributes, 'attr' point to the desired method        

        # Finally return the result of 'method' when using it with kwargs
        return method(**kwargs)



