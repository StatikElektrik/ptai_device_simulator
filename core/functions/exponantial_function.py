"""
This module calculates the exponantial function of a number.
"""
import numpy as np

from .interface import BaseFunction

class ExponantialFunction(BaseFunction):
    """This class calculates the exponantial function of a number."""

    def __init__(self, base: float, shift: float = 0.0, offset: float = 0.0) -> None:
        """Initialize the class.
        The function is defined as:
            y = offset + base^(x + shift)

        Parameters
        ----------
        base : float
            The base of the exponantial function.
        shift : float, optional
            The shift of the exponantial function, by default 0.0.
        offset : float, optional
            The offset of the exponantial function, by default 0.0.
        """
        super().__init__()
        self._base = base
        self._shift = shift
        self._offset = offset

    def calculate(self, x: float) -> float:
        """Calculate the exponantial function for a given x.

        Parameters
        ----------
        x : float
            The x value.

        Returns
        -------
        float
            The y value.
        """
        return self._offset + self._base ** (x + self._shift)

    def inverse(self, y: float) -> float:
        """Calculate the inverse of the exponantial function for a given y.

        Parameters
        ----------
        y : float
            The y value.

        Returns
        -------
        float
            The x value.
        """
        return np.log(y - self._offset) / np.log(self._base) - self._shift