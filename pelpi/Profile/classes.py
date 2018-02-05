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
        self._profile   = profile
        self._fwhm      = fwhm
        self._radius   = radius

        # self._checkInput(variable_dictionnary={\
        #     'time_profile':str,'space_profile':str,\
        #     'time_fwhm':type(_u('s')),
        #     'space_fwhm':type(_u('m')),'space_radius':type(_u('m')),\
        #     }) # TODO: How to do this with NoneType object ?

    def profile(self):
        """
        """
        return self._profile

    def fwhm(self):
        """
        """
        return self._fwhm

    def radius(self):
        """
        """
        return self._radius

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
    #         t0=self.time_fwhm()/(2 * _np.sqrt(_np.log(2)))
    #         return _np.exp(-(t/t0)**2)

    def envelope(self,r):
        """
        Returns
        -------
        Space pulse envelope at given radius : dimensionless quantity

        Parameters
        ----------
        r : length quantity
            Radius.

        Notes
        -----
        spaceEnvelope is centered at r=0 and has a maximum value of 1.
        """
        if self.profile()=="gaussian1D":
            t0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(r/t0)**2)

        if self.profile()=="gaussian2D":
            r0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            return _np.exp(-(r/r0)**2)
        elif self.profile()=="supergaussian":
            n=10
            return _np.exp(-(2*_np.sqrt(_np.log(2))*r/self.fwhm())**(2*n))
        elif self.profile()=="top-hat":
            if abs(r)<self.radius():
                return 1.0
            else:
                return 0.0


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

        .. math:: S_0^t = \sqrt{\pi} \\frac{t_{FWHM}}{2 \sqrt{\ln{2}}}

        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.profile()=="gaussian1D":
            t0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            S0t=t0 * _np.sqrt(_np.pi)
            return S0t
        else:
            raise NameError("Unknown laser time profile name.")

    def integral2D(self,lower_edge=None,upper_edge=None,number_points=None):
        """
        Returns
        -------
        Double integration of the space envelope under radius: length**2 quantity

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

        .. math:: S_r^0 = \pi (\\frac{r_{FWHM}}{2 \sqrt{\ln{2}}})^2

        ``top-hat`` :

        .. math:: S_r^0 = \pi r^2


        For other profiles, numerical integration is performed with numpy.trapz,
        so ``lower_edge``, ``upper_edge`` and ``number_points`` must be defined.
        """
        if self.profile()=="gaussian2D":
            r0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            S0r=_np.pi * r0**2
            return S0r
        elif self.profile()=="top-hat":
            return _np.pi*self.radius()**2
        else:
            raise NameError("Unknown laser space profile name.")
