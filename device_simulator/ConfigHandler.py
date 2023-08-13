import configparser
import os
import logging

logger = logging.getLogger('ConfigHandler')

def read_platform_config(config_file_name):
    config_content = {}
    config = configparser.ConfigParser()

    # Check if the config file exists
    config_file = config_file_name
    if not os.path.exists(config_file):
        logging.error("Config file '{}' not found.".format(config_file))
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
        logging.error("Config file '{}' not found.".format(config_file))
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