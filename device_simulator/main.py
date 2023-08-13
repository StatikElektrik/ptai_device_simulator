import logging
import random
import sys
import time

import ConfigHandler
from Device import Device
import DataGenerator
from IoTPlatform import IoTPlatform

PLATFORM_CONFIG_NAME = 'thingsboard_conf.ini'
DEVICE_CONFIG_NAME = 'thingsboard_conf.ini'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_args():
    if len(sys.argv) < 2:
        print("Usage: python main.py <MAC Address> [device token]")
        sys.exit(1)

    # First argument (mandatory): MAC Address
    mac_address = sys.argv[1]
    logging.info("MAC Address:", mac_address)

    # Second argument (optional): Device Token
    device_token = None
    if len(sys.argv) >= 3:
        device_token = sys.argv[2]
        logging.info("Device Token:", device_token)

    return mac_address, device_token


if __name__ == '__main__':

    mac_address, device_token = read_args()

    platform_config = ConfigHandler.read_platform_config(PLATFORM_CONFIG_NAME)
    device_config = ConfigHandler.read_device_config(DEVICE_CONFIG_NAME)
    iot_platform = IoTPlatform(platform_config["host"], platform_config["port"])

    start_points = [random.randint(0, 10) for _ in range(5)]
    random_generators = [DataGenerator.RandomGenerator(start_point) for start_point in start_points]

    simulated_device = Device(mac_address, '0.0.1', device_config["provision_key"],
                              device_config["provision_secret"])
    if device_token:
        simulated_device.set_token(device_token)

    if not simulated_device.is_registered:
        device_token = iot_platform.request_provision(simulated_device.name, simulated_device.provision_key,
                                                      simulated_device.provision_secret)
        simulated_device.set_token(device_token)

        iot_platform.send_attribute_data(simulated_device.token, simulated_device.to_dict())

    while True:
        iot_platform.send_telemetry_data(simulated_device.token,
                                         DataGenerator.generate_analysis_data(random_generators))
        time.sleep(random.randint(10, 60))
