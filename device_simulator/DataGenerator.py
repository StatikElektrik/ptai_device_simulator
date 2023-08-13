import random
import logging

logger = logging.getLogger('DataGenerator')

class RandomGenerator:
    def __init__(self, start_point):
        self.start_point = start_point

    def generate_random_array(self, array_size):  # Random array size between 1 and 10
        random_array = [random.randint(self.start_point, self.start_point + 20) for _ in range(array_size)]
        self.start_point += random.randint(1, 10)
        return random_array


def generate_analysis_data(random_generators):
    data_points_number = random.randint(1, 10)

    analysis_data = {
        "np": data_points_number,
        "e1": random_generators[0].generate_random_array(data_points_number),
        "e2": random_generators[1].generate_random_array(data_points_number),
        "e3": random_generators[2].generate_random_array(data_points_number),
        "e4": random_generators[3].generate_random_array(data_points_number),
        "e5": random_generators[4].generate_random_array(data_points_number),
    }

    return analysis_data
