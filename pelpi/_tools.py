
from . import verbose as _vb
from . import prefered_unit as _pu


__all__ = ["_Estimate"]

# class _Estimate(object):
#     """
#     Base class for estimations
#
#     Methods
#     ------
#     checkHypotheses
#         print informations about model hypotheses,
#         if verbose=True
#         if verbose=False
#     """
#     def __init__(self):
#         pass
#
#     def checkHypotheses(self):
#         pass
#
#     def useModel(self,package,model,method,available_models,dim,**kwargs):
#         # if type(package)!=module:
#         #     raise TypeError("package needs to be a pelpi module, but it is a"+str(type(package)))
#         # if type(model)!=str:
#         #     raise TypeError("model needs to be a string, but it is a"+str(type(model))) # TODO: why it is a type ?
#         # if type(method)!=function: # ??
#         #     raise TypeError("method needs to be a function, but it is a"+str(type(method)))
#         # if type(available_models)!=dict:
#         #     raise TypeError("available_models needs to be a dictionnary, but it is a"+str(type(available_models)))
#         # if type(dim)!=str:
#         #     raise TypeError("dim needs to be a string, but it is a"+str(type(dim)))
#
#         if model in available_models:
#             Model=_m.__dict__.get(model)(self._lpi)
#
#             Model.checkHypotheses()
#             return Model.method(**kwargs).to(_pu[dim])
#         else:
#             raise NameError("Model name "+model+" not found. Please refer to the documentation.")


class _Estimate(object):
    """
    Base class for estimations

    Methods
    ------
    checkHypotheses
        print informations about model hypotheses,
        if verbose=True
        if verbose=False
    """
    def __init__(self,LaserPlasmaInteraction,module,model):
        # if type(package)!=module:
        #     raise TypeError("package needs to be a pelpi module, but it is a"+str(type(package)))
        # if type(method)!=function: # ??
        #     raise TypeError("method needs to be a function, but it is a"+str(type(method)))
        # if type(available_models)!=dict:
        #     raise TypeError("available_models needs to be a dictionnary, but it is a"+str(type(available_models)))
        # self.verbose    = verbose # TODO: needed ?
        self._lpi       = LaserPlasmaInteraction
        # if model in available_models: # TODO: if the test is done, only available_models can be used (safer) but arg more
        self.model=module.__dict__.get(model)(self._lpi)
        # else:
        #     raise NameError("Model name "+model+" not found. Please refer to the documentation.")

    def checkHypotheses(self):
        self.model.checkHypotheses()

    def use(self,method,dim,**kwargs):
        # if type(model)!=str:
        #     raise TypeError("model needs to be a string, but it is a"+str(type(model))) # TODO: why it is a type ?
        # if type(dim)!=str:
        #     raise TypeError("dim needs to be a string, but it is a"+str(type(dim)))

        # self.model.checkHypotheses(_vb)
        self.model.checkHypotheses()
        self.model.__dict__.get(method)(**kwargs).to(_pu[dim])


# class _Estimate(object):
#     """
#     Base class for estimations
#
#     Methods
#     ------
#     checkHypotheses
#         print informations about model hypotheses,
#         if verbose=True
#         if verbose=False
#     """
#     def __init__(self,objet,model,available_models):
#         # if type(package)!=module:
#         #     raise TypeError("package needs to be a pelpi module, but it is a"+str(type(package)))
#         # if type(method)!=function: # ??
#         #     raise TypeError("method needs to be a function, but it is a"+str(type(method)))
#         # if type(available_models)!=dict:
#         #     raise TypeError("available_models needs to be a dictionnary, but it is a"+str(type(available_models)))
#         self.verbose    = verbose # TODO: needed ?
#         self._lpi       = LaserPlasmaInteraction
#         if model in available_models:
#             self.model=module.__dict__.get(model)(self._lpi)
#         else:
#             raise NameError("Model name "+model+" not found. Please refer to the documentation.")
#
#     def checkHypotheses(self):
#         pass
#
#     def use(self,method,dim,**kwargs):
#         # if type(model)!=str:
#         #     raise TypeError("model needs to be a string, but it is a"+str(type(model))) # TODO: why it is a type ?
#         # if type(dim)!=str:
#         #     raise TypeError("dim needs to be a string, but it is a"+str(type(dim)))
#
#         if model in available_models:
#             Model=_m.__dict__.get(model)(self._lpi)
#
#             Model.checkHypotheses(self.verbose)
#             return Model.method(**kwargs).to(_pu[dim])
#         else:
#             raise NameError("Model name "+model+" not found. Please refer to the documentation.")
