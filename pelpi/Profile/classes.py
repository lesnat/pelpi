#coding:utf8
from .._global import *
from .._tools import _PelpiObject


class Profile(_PelpiObject):
    """
    Class for defining spatial and temporal pulse profiles.

    Yet only simple profiles are accepted (depends only on radius).

    Parameters
    ---------
    time_profile : str
        Temporal profile of the pulse. Available : ``gaussian``
    space_profile : str
        Spatial profile of the pulse (waist). Available : ``gaussian``, ``top-hat``

    time_fwhm : time quantity, optional
        Temporal Full Width Half Maximum of the laser pulse.
    space_fwhm : length quantity, optional
        Spatial Full Width Half Maximum of the laser pulse.
    space_radius : length quantity, optional
        Spatial radius of the laser pulse.

    Notes
    -----
    If ``time_profile`` is ``gaussian``, you must define ``time_fwhm``.

    If ``space_profile`` is ``gaussian``, you must define ``space_fwhm``.

    If ``space_profile`` is ``top-hat``, you must define ``space_radius``.


    Examples
    --------
    You can set a laser profile as follows :

    >>> import pelpi as pp
    >>> prof = pp.Profile(
    ...    time_profile  = "gaussian",
    ...    time_fwhm     = 30 * pp.unit('fs'),
    ...    space_profile = "top-hat",
    ...    space_radius  = 10 * pp.unit('um')
    ...    )
    ...
    """
    def __init__(self,profile,fwhm=None,radius=None):
        self.default            = {}
        self.default['profile'] = profile
        self.default['fwhm']    = fwhm
        self.default['radius']  = radius

        # self._checkInput(variable_dictionnary={\
        #     'time_profile':str,'space_profile':str,\
        #     'time_fwhm':type(_u('s')),
        #     'space_fwhm':type(_u('m')),'space_radius':type(_u('m')),\
        #     }) # TODO: How to do this with NoneType object ?

    def profile(self):
        """
        """
        return self.default['profile']

    def fwhm(self):
        """
        """
        return self.default['fwhm']

    def radius(self):
        """
        """
        return self.default['radius']

    # def timeEnvelope(self,t):
    #     """
    #     Returns
    #     -------
    #     Time pulse envelope at given time : dimensionless quantity
    #
    #     Parameters
    #     ----------
    #     t : time quantity
    #         Time.
    #
    #     Notes
    #     -----
    #     timeEnvelope is centered at t=0, and has a maximum value of 1.
    #     """
    #     if self.time_profile()=="gaussian":
    #         x0=self.time_fwhm()/(2 * _np.sqrt(_np.log(2)))
    #         return _np.exp(-(t/x0)**2)

    def envelope(self,x):
        """
        Returns
        -------
        Profile envelope at x : dimensionless quantity

        Parameters
        ----------
        x : quantity (length or time)

        Notes
        -----
        envelope is centered at x=0 and has a maximum value of 1.
        """
        if self.profile()=="gaussian1D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(x/x0)**2) * _u('')

        if self.profile()=="gaussian2D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(x/x0)**2) * _u('')
        elif self.profile()=="top-hat":
            if abs(x)<self.radius():
                return 1.0 * _u('')
            else:
                return 0.0 * _u('')


    def integral1D(self,lower_edge=None,upper_edge=None,number_points=None):
        """
        Returns
        -------
        Integration of timeEnvelope under time : time quantity

        Parameters
        ----------
        lower_edge : float, optional
            Lower edge of integration
        upper_edge : float, optional
            Upper edge of integration
        number_points : int, optional
            Number of points to use

        Notes
        -----
        Some analytical solutions exists for time profiles :

        ``gaussian`` :

        .. math:: I_x = \sqrt{\pi} \\frac{t_{FWHM}}{2 \sqrt{\ln{2}}}

        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.profile()=="gaussian1D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            Ix=x0 * _np.sqrt(_np.pi)
            return Ix
        else:
            raise NameError("Unknown laser time profile name.")

    def integral2D(self,lower_edge=None,upper_edge=None,number_points=None):
        """
        Returns
        -------
        Double integration of the envelope under x: quantity

        Parameters
        ----------
        lower_edge : float, optional
            Lower edge of integration
        upper_edge : float, optional
            Upper edge of integration
        number_points : int, optional
            Number of points to use

        Notes
        -----
        Some analytical solutions exists for space profiles :

        ``gaussian`` :

        .. math:: I_x = \pi (\\frac{x_{FWHM}}{2 \sqrt{\ln{2}}})^2

        ``top-hat`` :

        .. math:: I_x = \pi x^2


        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.profile()=="gaussian2D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            Ix=_np.pi * x0**2
            return Ix
        elif self.profile()=="top-hat":
            return _np.pi*self.radius()**2
        else:
            raise NameError("Unknown laser space profile name.")
