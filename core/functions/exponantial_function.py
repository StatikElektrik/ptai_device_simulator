"""
This module calculates the exponantial function of a number.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar


class ExponentialFunction:
    """
    A class representing an exponential function of the form f(x) = b^(x - h) + k.
    """

    def __init__(self, base: float, shift: float, offset: float):
        """
        Initialize the ExponentialFunction object.

        :param base: Base parameter of the exponential function.
        :param shift: Shift in x direction of the exponential function.
        :param offset: Shift in y direction of the exponential function.
        """
        self.base = base
        self.x_shift = shift
        self.y_shift = offset

    def __str__(self) -> str:
        return f"f(x) = {self.base}^(x - {self.x_shift}) + {self.y_shift}"

    def _calculate_y(self, x_values: np.ndarray) -> np.ndarray:
        """
        Calculate the y value of the exponential function for a given x.

        :param x: The input x value.
        :return: The calculated y value.
        """
        return self.base ** (x_values - self.x_shift) + self.y_shift

    def plot_function(self, x_range: tuple[float, float]) -> None:
        """
        Plot the exponential function within the specified x range.

        :param x_range: A tuple representing the start and end values of the x range.
        """
        x_values = np.linspace(x_range[0], x_range[1], 1000)
        y_values = self._calculate_y(x_values)

        plt.plot(x_values, y_values)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title(f"Exponential Function: {self}")
        plt.grid(True)
        plt.show()

    def find_x_for_y(
        self, target_y: np.ndarray, x_range: tuple[float, float]
    ) -> np.ndarray:
        """
        Find the x values for given target y values within the specified x range.

        :param target_y: An array of target y values.
        :param x_range: A tuple representing the start and end values of the x range.
        :return: An array of calculated x values.
        """

        def error_func(x_values: np.ndarray) -> np.ndarray:
            return self._calculate_y(x_values) - target_y

        try:
            result = root_scalar(error_func, bracket=x_range, method="brentq")
            return result.root
        except ValueError:
            print("No root found in the given range.")


# Örnek kullanım:
b_value: float = 2.0
h_value: float = 1.0
k_value: float = 3.0

exp_function: ExponentialFunction = ExponentialFunction(b_value, h_value, k_value)
exp_function.plot_function((-10.0, 10.0))

x_value: float = 2.0
y_value: float = exp_function._calculate_y(x_value)
print(f"f({x_value}) = {y_value}")

target_y: float = 5.0
x_range: tuple[float, float] = (-10.0, 10.0)
x_for_target_y: float = exp_function.find_x_for_y(target_y, x_range)
print(f"For y = {target_y}, x = {x_for_target_y}")
