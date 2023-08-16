"""
This module is responsible for reading the configuration files.
"""

import configparser
import os
import logging

# Create a logger interface.
logger = logging.getLogger(__name__)


class ConfigHandler:
    """This class is responsible for reading the configuration files."""
    # @TODO: Add a wrapper interface to minimize the code.

    @staticmethod
    def read_platform_config(file_location: str) -> dict:
        """It reads the platform configuration file and returns a dictionary with the content.

        Parameters
        ----------
        file_location : str
            The name of the configuration file. It must be a .ini file.

        Returns
        -------
        dict
            A dictionary with the content of the configuration file.
            - host : str
                The host of the platform.
            - port : str
                The port of the platform.
        """
        config_content = {}
        config = configparser.ConfigParser()

        # Check if the config file exists.
        if not os.path.exists(file_location):
            logger.error("Config file '%s' not found.", file_location)
            raise FileNotFoundError("Config file not found.")

        try:
            config.read(file_location)
            # Read connection section.
            config_content["host"] = config.get("Connection", "host")
            config_content["port"] = config.get("Connection", "port")
        except Exception as error:
            logger.error("An error occurred while reading the config file: %s", error)
            raise error

        # Return the content of the config file.
        return config_content

    @staticmethod
    def read_device_config(file_location: str) -> dict:
        """It reads the device configuration file and returns a dictionary with the content.

        Parameters
        ----------
        file_location : str
            The name of the configuration file. It must be a .ini file.

        Returns
        -------
        dict
            A dictionary with the content of the configuration file.
            - provision_key : str
                The provision key of the device.
            - provision_secret : str
                The provision secret of the device.
        """
        config_content = {}
        config = configparser.ConfigParser()

        # Check if the config file exists.
        if not os.path.exists(file_location):
            logging.error("Config file '%s' not found.", file_location)
            raise FileNotFoundError("Config file not found.")

        try:
            config.read(file_location)
            # Read connection section
            config_content["provision_key"] = config.get("Device", "provision_key")
            config_content["provision_secret"] = config.get(
                "Device", "provision_secret"
            )
        except Exception as error:
            logger.error("An error occurred while reading the config file: %s", error)
            raise error

        # Return the content of the config file.
        return config_content
