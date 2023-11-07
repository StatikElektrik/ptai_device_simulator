"""
This module is responsible for reading the configuration files.
"""

import logging
from os import getenv
from dotenv import load_dotenv

from .argument_handler import ArgumentHandler

# Create a logger interface.
logger = logging.getLogger(__name__)


class ConfigHandler:
    """This class is responsible for reading the configuration files."""

    @staticmethod
    def read() -> dict[str, str]:
        """It reads the configuration file and return the variables needed.

        Returns
        -------
        dict[str, str]
            A dictionary with the content of the configuration file.
            - host : str
                The host of the platform.
            - port : str
                The port of the platform.
            - provision_key : str
                The provision key of the device.
            - provision_secret : str
                The provision secret of the device.
        """
        # Load the environment variables.
        load_dotenv()

        # Read the arguments passed to the program.
        args = ArgumentHandler.read()

        # Create a dictionary to store the content of the config file.
        config_content: dict[str, str] = {}

        # Read connection section.
        config_content["host"] = getenv("THINGSBOARD_HOST", args.host)
        config_content["port"] = getenv("THINGSBOARD_PORT", args.port)

        #  Read device section
        config_content["mac_addr"] = getenv("DEVICE_MAC_ADDR", args.mac_addr)
        config_content["token"] = getenv("DEVICE_TOKEN", args.token)
        config_content["provision_key"] = getenv(
            "DEVICE_PROVISION_KEY", args.provision_key
        )
        config_content["provision_secret"] = getenv(
            "DEVICE_PROVISION_SECRET", args.provision_secret
        )

        # Return the content of the config file.
        return config_content
