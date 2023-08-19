"""
This module is responsible for generating random data for the analysis.
"""
import logging
from typing import Any
from numpy import random
from .functions.exponantial_function import ExponantialFunction

# Create a logger interface.
logger = logging.getLogger(__name__)


class DataGenerator:
    """This class is responsible for generating data format for the analysis
    just like recieved from MCU.
    """

    SUPPORTED_FUNCTIONS = [
        {
            "name": "exponantial",
            "class": ExponantialFunction,
            "parameters": ["base", "shift", "offset"],
        },
    ]

    def __init__(
        self,
        buffer_size: int,
        function_type: str,
        function_parameters: dict[str, float],
        data_index: int = 0,
    ) -> None:
        # Check if the function type is valid.
        if function_type not in [func["name"] for func in self.SUPPORTED_FUNCTIONS]:
            raise ValueError(
                f"Function type {function_type} is not supported. "
                f"Supported functions are {self.SUPPORTED_FUNCTIONS}"
            )

        # Check if the function parameters are valid.
        for parameter in function_parameters:
            if parameter not in [
                func["parameters"] for func in self.SUPPORTED_FUNCTIONS
            ]:
                raise ValueError(
                    f"Parameter {parameter} is not supported. "
                    f"Supported parameters are {self.SUPPORTED_FUNCTIONS}"
                )

        # Create the function object.
        self.function = self._create_function(function_type, function_parameters)

        # Set the data index and buffer size.
        self._data_index = data_index
        self._buffer_size = buffer_size


    def generate(self, step_size: int = 1, add_error: int = 0) -> list[float]:
        """Generate the data.

        Returns
        -------
        list[float]
            The generated data.
        """
        x_values = [self._data_index + i for i in range(0, self._buffer_size, step_size)]
        y_values = [self.function.calculate(x) for x in x_values]
        self._data_index += self._buffer_size

        # Add error to the data.
        if add_error > 0:
            error_percentage = add_error / 100
            y_values = self._add_error(y_values, error_percentage)

        return y_values

    @staticmethod
    def _add_error(y_values: list[float], error_percentage: float) -> list[float]:
        """Add error to the data.

        Parameters
        ----------
        y_values : list[float]
            The y values.
        error_percentage : float
            The error percentage.

        Returns
        -------
        list[float]
            The y values with error.
        """
        random_error_multiplier = random.randn(0, error_percentage)
        return [y + (y * random_error_multiplier) for y in y_values]

    @staticmethod
    def _create_function(f_type: str, f_params: dict[str, Any]):
        """Create the function object.

        Parameters
        ----------
        f_type : str
            The type of the function.
        f_params : dict[str, Any]
            The parameters of the function.

        Returns
        -------
        BaseFunction
            The function object.
        """
        for func in DataGenerator.SUPPORTED_FUNCTIONS:
            if func["name"] == f_type:
                return func["class"](**f_params)
