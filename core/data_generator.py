"""
This module is responsible for generating random data for the analysis.
"""
import logging
from typing import Any
from random import randint
from math import floor
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
        params_available: list
        for func in self.SUPPORTED_FUNCTIONS:
            if func["name"] == function_type:
                params_available = func["parameters"]

        for parameter in function_parameters:
            if parameter not in params_available:
                raise ValueError(
                    f"Parameter {parameter} is not supported. "
                    f"Supported parameters are {self.SUPPORTED_FUNCTIONS}"
                )

        # Create the function object.
        self.function = self._create_function(function_type, function_parameters)

        # Set the data index and buffer size.
        self._data_index = data_index
        self._buffer_size = buffer_size

    def generate(self, step_size: float = 0.01, error_percentage: int = 0) -> list[float]:
        """Generate the data.

        Returns
        -------
        list[float]
            The generated data.
        """
        x_values = [self._data_index + (step_size * i) for i in range(self._buffer_size)]
        y_values = [self.function.calculate(x) for x in x_values]
        self._data_index += self._buffer_size

        # Add error to the data.
        if error_percentage > 0:
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
        # @TODO: Implement with numpy for better performance.
        errored_y_values: list[float] = []
        for y_value in y_values:
            random_error_multiplier = randint(0, floor(error_percentage))
            random_sign = randint(0, 1)
            sign_multiplier = 1 if random_sign == 0 else -1
            errored_y = y_value + sign_multiplier * (y_value * (random_error_multiplier / 100))
            errored_y_values.append(errored_y)
        return errored_y_values

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
