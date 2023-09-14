"""
This class is the base class for all the function
implementations. It defines the interface that all
subclasses must implement.
"""

from abc import ABC, abstractmethod
from matplotlib import pyplot as plt

class BaseFunction(ABC):
    """Follow this interface to implement a function for
    DataGenerator.
    """

    @abstractmethod
    def calculate(self, x_value: float) -> float:
        """The interface function to calculate the function."""

    @abstractmethod
    def inverse(self, y_value: float) -> float:
        """The interface function to calculate the inverse of the function."""

    @staticmethod
    def plot(x_values: list, y_values: list, plot_type="linear") -> None:
        """This function is used to plot the function. Do not
        implement this function in the subclass. This function
        is implemented in the base class to provide a common
        interface for all the subclasses.

        Parameters
        ----------
        x_values : list
            The inputs to the function.
        y_values : list
            The outputs of the function.
        plot_type : str, optional
            "linear", "exponantial", "dbscale", by default "linear"
        """

        if plot_type == "linear":
            # Plot the function in linear scale.
            plt.plot(x_values, y_values)
            plt.x_label("x_values")
            plt.y_label("y_values")
            plt.title("Linear Scale Plot of The Function")
            plt.show()
        else:
            raise NotImplementedError
