"""
This module is responsible for generating random data for the analysis.
"""
import random
import logging

# Create a logger interface.
logger = logging.getLogger(__name__)


class DataGenerator:
    """This class is responsible for generating data format for the analysis
    just like recieved from MCU.
    """

    def __init__(
        self,
        buffer_size: int,
        function_type: str,
        function_parameters: dict[str, float],
    ) -> None:
        self.buffer_size = buffer_size

    def generate(self) -> list:
        """@TODO: What is this?"""
        return [random.randint(0, 100) for _ in range(self.buffer_size)

    def _calculate_max_element(self, frequency: int, duration: int) -> int:
        """@TODO: What is this?"""

    def _add_error_to_data(self, data: list, error_percentage: int) -> list:
        """@TODO: What is this?"""

    def _calculate_function_value(self, time_val: int) -> float:
        """@TODO: What is this?"""
