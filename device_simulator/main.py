import logging
import asyncio
import os
import random
import time

from aiocoap import Context, Message, Code
import json
import configparser

THINGSBOARD_HOST = "coap.thingsboard.cloud"
THINGSBOARD_PORT = "5683"

PLATFORM_CONFIG_NAME = 'thingsboard_conf.ini'
DEVICE_CONFIG_NAME = 'thingsboard_conf.ini'

logging.basicConfig(level=logging.INFO)


def read_platform_config(config_file_name):
    config_content = {}
    config = configparser.ConfigParser()

    # Check if the config file exists
    config_file = config_file_name
    if not os.path.exists(config_file):
        print("Config file '{}' not found.".format(config_file))
        return None

    try:
        config.read(config_file)

        # Read connection section
        config_content["host"] = config.get('Connection', 'host')
        config_content["port"] = config.get('Connection', 'port')

    except Exception as e:
        print("An error occurred while reading the config file:", str(e))
        return None

    return config_content


def read_device_config(config_file_name):
    config_content = {}
    config = configparser.ConfigParser()

    # Check if the config file exists
    config_file = config_file_name
    if not os.path.exists(config_file):
        print("Config file '{}' not found.".format(config_file))
        return None

    try:
        config.read(config_file)

        # Read connection section
        config_content["provision_key"] = config.get('Device', 'provision_key')
        config_content["provision_secret"] = config.get('Device', 'provision_secret')

    except Exception as e:
        print("An error occurred while reading the config file:", str(e))
        return None

    return config_content


# Example for message to ThingsBoard
to_publish = {
    "stringKey": "value1",
    "booleanKey": True,
    "doubleKey": 42.0,
    "longKey": 73,
    "jsonKey": {
        "someNumber": 42,
        "someArray": [1, 2, 3],
        "someNestedObject": {"key": "value"}
    }
}


class Modem:
    def __init__(self, IMEI='FFFFFFFFFFFFFFFF', fw_ver='0'):
        self.IMEI = IMEI
        self.fw_ver = fw_ver


class SimCard:
    def __init__(self, ICCID='FFFFFFFFFFFFFFFFFFFF', IMSI='FFFFFFFFFFF'):
        self.ICCID = ICCID
        self.IMSI = IMSI


class Device:
    def __init__(self, name, fw_version, provision_key, provision_secret):
        self.name = name
        self.state = 0
        self.error = 0
        self.is_registered = False
        self.fw_version = fw_version
        self.provision_key = provision_key
        self.provision_secret = provision_secret
        self.token = None
        self.modem = Modem()
        self.sim_card = SimCard()

    def set_token(self, token):
        self.token = token

    def to_dict(self):
        return {
            "name": self.name,
            "state": self.state,
            "error": self.error,
            "is_registered": self.is_registered,
            "IMEI": self.modem.IMEI,
            "modem_fw": self.modem.fw_ver,
            "ICCID": self.sim_card.ICCID,
            "IMSI": self.sim_card.IMSI
        }


class IoTPlatform:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def request_provision(self, device_name, device_provision_key, device_provision_secret):
        received_token = asyncio.run(self.request_provision_async(device_name, device_provision_key, device_provision_secret))
        return received_token

    async def request_provision_async(self, device_name, device_provision_key, device_provision_secret):
        received_token = None

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)
        try:

            server_address = "coap://" + self.hostname + ':' + self.port
            provision_request = {"provisionDeviceKey": device_provision_key,
                                 "provisionDeviceSecret": device_provision_secret,
                                 "deviceName": device_name,
                                 }

            msg = Message(code=Code.POST, payload=str.encode(json.dumps(provision_request)),
                          uri=server_address + '/api/v1/provision')
            request = client_context.request(msg)
            try:
                response = await asyncio.wait_for(request.response, 60000)
            except asyncio.TimeoutError:
                raise Exception("Request timed out!")

            if response is None:
                raise Exception("Response is empty!")

            decoded_response = json.loads(response.payload)
            logging.info("Received response: %s", decoded_response)
            received_token = decoded_response.get("credentialsValue")
            if received_token is None:
                logging.error("Failed to get access token from response.")
                logging.error(decoded_response.get("errorMsg"))
        except Exception as e:
            logging.error(e)
        finally:
            await client_context.shutdown()
            return received_token

    def send_telemetry_data(self, device_token, data):
        asyncio.run(self.send_telemetry_data_async(device_token, data))

    async def send_telemetry_data_async(self, device_token, data):
        server_address = "coap://" + self.hostname + ':' + self.port

        msg = Message(code=Code.POST, payload=str.encode(json.dumps(data)),
                      uri=server_address + ('/api/v1/%s/telemetry' % device_token))

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)

        request = client_context.request(msg)
        try:
            response = await asyncio.wait_for(request.response, 60000)
        except asyncio.TimeoutError:
            raise Exception("Request timed out!")
        finally:
            await client_context.shutdown()

        if response:
            logging.info("[THINGSBOARD CLIENT] Response from Thingsboard.")
            logging.info(response)
        else:
            raise Exception("[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!")

    def send_attribute_data(self, device_token, data):
        asyncio.run(self.send_attribute_data_async(device_token, data))

    async def send_attribute_data_async(self, device_token, data):
        server_address = "coap://" + self.hostname + ':' + self.port

        msg = Message(code=Code.POST, payload=str.encode(json.dumps(data)),
                      uri=server_address + ('/api/v1/%s/attributes' % device_token))

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)

        request = client_context.request(msg)
        try:
            response = await asyncio.wait_for(request.response, 60000)
        except asyncio.TimeoutError:
            raise Exception("Request timed out!")
        finally:
            await client_context.shutdown()

        if response:
            logging.info("[THINGSBOARD CLIENT] Response from Thingsboard.")
            logging.info(response)
        else:
            raise Exception("[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!")


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


if __name__ == '__main__':

    platform_config = read_platform_config(PLATFORM_CONFIG_NAME)
    device_config = read_device_config(DEVICE_CONFIG_NAME)

    simulated_device = Device('40ED98AABBC3', '0.0.1', device_config["provision_key"],
                              device_config["provision_secret"])
    iot_platform = IoTPlatform(platform_config["host"], platform_config["port"])

    start_points = [random.randint(0, 10) for _ in range(5)]
    random_generators = [RandomGenerator(start_point) for start_point in start_points]

    if not simulated_device.is_registered:
        device_token = iot_platform.request_provision(simulated_device.name, simulated_device.provision_key, simulated_device.provision_secret)
        simulated_device.set_token(device_token)

        iot_platform.send_attribute_data(simulated_device.token, simulated_device.to_dict())

    while True:
       iot_platform.send_telemetry_data(simulated_device.token,generate_analysis_data(random_generators))
       time.sleep(random.randint(10, 60))
