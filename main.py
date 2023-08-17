"""
The main file of the simulated device. It is responsible for:
    - Reading the MAC Address and Device Token from the command line
    - Creating a simulated device
    - Registering the device on the IoT platform
    - Sending telemetry data to the IoT platform
"""
import logging
import random
import sys
import time

# Import all the core modules.
from core import ConfigHandler, DataGenerator, RandomGenerator
from core import Device, ThingsboardConnector


# Create a custom logger interface.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Read the configurations.
    config = ConfigHandler.read()

    connector = ThingsboardConnector(config["host"], config["port"])

    start_points = [random.randint(0, 10) for _ in range(5)]
    random_generators = [RandomGenerator(start_point) for start_point in start_points]

    simulated_device = Device(
        mac, "0.0.1", config["provision_key"], config["provision_secret"]
    )
    if token:
        simulated_device.set_token(token)

    if not simulated_device.is_registered:
        token = connector.request_provision(
            simulated_device.name,
            simulated_device.provision_key,
            simulated_device.provision_secret,
        )
        simulated_device.set_token(token)

        connector.send_attribute_data(
            simulated_device.token, simulated_device.to_dict()
        )

    while True:
        connector.send_telemetry_data(
            simulated_device.token,
            DataGenerator.generate_analysis_data(random_generators),
        )
        time.sleep(random.randint(10, 60))
