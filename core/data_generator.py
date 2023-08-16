"""
This module is responsible for generating random data for the analysis.
"""
import random
import logging

# Create a logger interface.
logger = logging.getLogger(__name__)


class RandomGenerator:
    """This class is responsible for generating random list for the analysis."""

    def __init__(self, start_point: float):
        self.start_point = start_point

    def generate_random_array(self, array_size: int):
        """It generates a random array with the given size.

        Parameters
        ----------
        array_size : int
            The size of the array to be generated. It must be in the range [1, 10].

        Returns
        -------
        list
            A list with the random values.
        """
        random_array = [
            random.randint(self.start_point, self.start_point + 20)
            for _ in range(array_size)
        ]
        self.start_point += random.randint(1, 10)
        return random_array


class DataGenerator:
    """This class is responsible for generating data format for the analysis
    just like recieved from MCU.
    """

    @staticmethod
    def generate_analysis_data(random_generators) -> dict:
        """It generates a dictionary with the analysis data.

        Parameters
        ----------
        random_generators : @TODO What is this?
            @TODO What is this?

        Returns
        -------
        dict
            A dictionary with the analysis data that can be thought
            as its recieved from MCU AI component.
        """
        data_points_number = random.randint(1, 10)
        return {
            "np": data_points_number,
            "e1": random_generators[0].generate_random_array(data_points_number),
            "e2": random_generators[1].generate_random_array(data_points_number),
            "e3": random_generators[2].generate_random_array(data_points_number),
            "e4": random_generators[3].generate_random_array(data_points_number),
            "e5": random_generators[4].generate_random_array(data_points_number),
        }
