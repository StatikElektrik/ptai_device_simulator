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

from core import (
    ConfigHandler,
    Device,
    DataGenerator,
    RandomGenerator,
    ThingsboardConnector,
)

# Constants
PLATFORM_CONFIG_NAME = "thingsboard_conf.ini"
DEVICE_CONFIG_NAME = "thingsboard_conf.ini"

# Create a custom logger interface.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def read_args() -> list:
    """
    Read the MAC Address and Device Token from the command line.

    Returns:
        mac_address (str): The MAC Address of the device.
        device_token (str): The Device Token of the device.
    """

    if len(sys.argv) < 2:
        print("Usage: python main.py <MAC Address> [device token]")
        sys.exit(1)

    # First argument (mandatory): MAC Address
    mac_address = sys.argv[1]
    # Second argument (optional): Device Token
    device_token = sys.argv[2] if len(sys.argv) >= 3 else None

    # Log the MAC Address and Device Token.
    logger.info("MAC Address: %s", mac_address)
    logger.info("Device Token: %s", device_token)

    return mac_address, device_token


if __name__ == "__main__":
    mac, token = read_args()

    platform_config = ConfigHandler.read_platform_config(PLATFORM_CONFIG_NAME)
    device_config = ConfigHandler.read_device_config(DEVICE_CONFIG_NAME)
    iot_platform = ThingsboardConnector(
        platform_config["host"], platform_config["port"]
    )

    start_points = [random.randint(0, 10) for _ in range(5)]
    random_generators = [RandomGenerator(start_point) for start_point in start_points]

    simulated_device = Device(
        mac, "0.0.1", device_config["provision_key"], device_config["provision_secret"]
    )
    if token:
        simulated_device.set_token(token)

    if not simulated_device.is_registered:
        token = iot_platform.request_provision(
            simulated_device.name,
            simulated_device.provision_key,
            simulated_device.provision_secret,
        )
        simulated_device.set_token(token)

        iot_platform.send_attribute_data(
            simulated_device.token, simulated_device.to_dict()
        )

    while True:
        iot_platform.send_telemetry_data(
            simulated_device.token,
            DataGenerator.generate_analysis_data(random_generators),
        )
        time.sleep(random.randint(10, 60))
