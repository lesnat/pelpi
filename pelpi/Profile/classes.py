#coding:utf8
from .._global import *
from .._tools import _PelpiObject

__all__=["Profile"]

class Profile(_PelpiObject):
    """
    Class for defining a geometrical profile.
    
    Used for defining Laser profiles (spatial and temporal)
    and might be used in Target object in the future.


    Parameters
    ---------
    profile : str
        Geometrical profile.
    fwhm : Quantity, optional
        Full Width Half Maximum of the profile.
    radius : Quantity, optional
        Radius of the profile.

    Notes
    -----
    Available profiles are
        ``gaussian1D``  : one dimension gaussian profile. It equals 1 for x=0.
        ``gaussian2D``  : two dimensions isotropic gaussian profile. It equals 1 for x=0.
        ``top-hat``     : two dimensions top-hat isotropic profile. It equals 1 if |x|<radius, 0 otherwise.
    
    If ``profile`` is ``gaussian1D``, you must define ``fwhm``.
    If ``profile`` is ``gaussian2D``, you must define ``fwhm``.
    If ``profile`` is ``top-hat``, you must define ``radius``.


    Examples
    --------
    You can set a laser time profile as follows

    >>> import pelpi as pp
    >>> tprof = pp.Profile(
    ...    profile  = "gaussian1D",
    ...    fwhm     = 30 * pp.unit('fs')
    ...    )
    ...
    """
    def __init__(self,profile=None,fwhm=None,radius=None):
        # Test user input
        self._check_input('profile' , profile   , str)
        self._check_input('fwhm'    , fwhm      , "<class 'pint.unit.Quantity'>") # Can be time or length
        self._check_input('radius'  , radius    , "<class 'pint.unit.Quantity'>") # Can be time or length
        
        # Initialize default dict
        self._initialize_defaults(input_dict={'profile':profile,'fwhm':fwhm,'radius':radius})


    def profile(self):
        """
        Returns
        -------
        User input `profile` : str
        """
        return self.default['profile']

    def fwhm(self):
        """
        Returns
        -------
        User input `fwhm` : Quantity
        """
        return self.default['fwhm']

    def radius(self):
        """
        Returns
        -------
        User input `radius` : Quantity
        """
        return self.default['radius']

    def envelope(self,x):
        """
        Returns
        -------
        Profile envelope at x : dimensionless Quantity

        Parameters
        ----------
        x : Quantity

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


    def integral1D(self):
        """
        Returns
        -------
        Integration of envelope under x : Quantity

        Notes
        -----
        Yet only analytical integrals are implemented, as the available profiles permit it.

        Analytical solutions are
            For ``gaussian1D``

            .. math:: I_x = \sqrt{\pi} \\frac{t_{FWHM}}{2 \sqrt{\ln{2}}}
        
        """
        if self.profile()=="gaussian1D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            Ix=x0 * _np.sqrt(_np.pi)
            return Ix
        else:
            raise NameError("Unknown laser time profile name.")

    def integral2D(self):
        """
        Returns
        -------
        Double integration of the envelope under x : Quantity

        Notes
        -----
        Yet only analytical integrals are implemented, as the available profiles permit it.

        Analytical solutions are

        For ``gaussian2D``

        .. math:: I_x = \pi (\\frac{x_{FWHM}}{2 \sqrt{\ln{2}}})^2

        For ``top-hat``

        .. math:: I_x = \pi r^2

        """
        if self.profile()=="gaussian2D":
            x0=self.fwhm()/(2 * _np.sqrt(_np.log(2)))
            Ix=_np.pi * x0**2
            return Ix
        elif self.profile()=="top-hat":
            return _np.pi*self.radius()**2
        else:
            raise NameError("Unknown laser space profile name.")
