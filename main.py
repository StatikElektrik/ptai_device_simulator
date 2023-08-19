"""
The main file of the simulated device. It is responsible for:
    - Reading the MAC Address and Device Token from the command line
    - Creating a simulated device
    - Registering the device on the IoT platform
    - Sending telemetry data to the IoT platform
"""
import logging
import random
import time

# Import all the core modules.
from core import ConfigHandler, DataGenerator
from core import Device, ThingsboardConnector

# Create a custom logger interface.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Read the configurations.
    config = ConfigHandler.read()

    # Create a ThingsboardConnector instance.
    connector = ThingsboardConnector(config["host"], config["port"])

    # Create a device instance.
    device = Device(config["mac_addr"])

    if config["token"]:
        # If the token is provided, set it to the device.
        # It means the device is already registered.
        device.set_token(config["token"])
    else:
        # If the token is not provided, set the provision key and secret.
        # It means the device is not registered. Use ThingsboardConnector
        # to register.
        device.set_provision_key(config["provision_key"])
        device.set_provision_secret(config["provision_secret"])
        connector.register_device(device)

    # Create a data generator function.
    sensor_1 = DataGenerator(5, "exponantial", {"base": 2.67, "offset": 25})
    sensor_2 = DataGenerator(3, "exponantial", {"base": 3.38, "shift": 0.12})

    # Create formatted data to be sent to the ThingSpeak.
    data_packet = device.get_formatted_data(
        "e1", sensor_1.generate(0.001, 25),
        "e2", sensor_2.generate(error_percentage=10),
    )

    # Send telemetry data to the IoT platform.
    while True:
        # @TODO: Send data only for the duration within a given frequency.
        connector.send_telemetry_data(device.get_token(), data_packet)
        time.sleep(random.randint(10, 60))
