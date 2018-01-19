
from . import prefered_unit as _pu


__all__ = ["_Estimate"]

class _Estimate(object):
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
        if str(type(LaserPlasmaInteraction))!="<class 'pelpi.LaserPlasmaInteraction.LaserPlasmaInteraction'>":
            raise TypeError("'LaserPlasmaInteraction' type must be a pelpi module, but it is "+str(type(LaserPlasmaInteraction)))
        if type(model_name)!=str:
            raise TypeError("'model_name' type must be 'string', but it is "+str(type(model_name)))
        if type(available_models)!=list:
            raise TypeError("'available_models' type must be 'list', but it is "+str(type(available_models)))

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

        # Check the model hypotheses
        self.model.checkHypotheses()
        # Get the method from the model
        Method = getattr(self.model,method_name)
        # Use it with kwargs and convert it
        return Method(*args).to(_pu[dim]) # TODO: check if OK with args


# def _addMethod(InObject,OutObject,method):
#     OutObject.__dict__.get(method) = InObject.__dict__.get(method)
