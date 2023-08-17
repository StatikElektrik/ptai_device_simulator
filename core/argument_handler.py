"""
This module is responsible for reading the arguments passed to the program.
"""

import logging
import argparse

# Create a logger interface.
logger = logging.getLogger(__name__)


class ArgumentHandler:
    """This class is responsible for reading the arguments passed to the program."""

    ARGUMENTS = {
        "--mac_addr": {
            "type": str,
            "nargs": "?",
            "help": "The MAC Address of the simulated device.",
            "dest": "mac_addr",
        },
        "--token": {
            "type": str,
            "nargs": "?",
            "help": "The token for CoAP connection. Will generate itself if not passed",
            "dest": "token",
        },
        "--host": {
            "type": str,
            "nargs": "?",
            "help": "The host of the CoAP platform.",
            "dest": "host",
        },
        "--port": {
            "type": str,
            "nargs": "?",
            "help": "The port of the CoAP platform.",
            "dest": "port",
        },
        "--provision_key": {
            "type": str,
            "nargs": "?",
            "help": "The provision key of the device. Necessary if token is not provided.",
            "dest": "provision_key",
        },
        "--provision_secret": {
            "type": str,
            "nargs": "?",
            "help": "The provision secret of the device. Necessary if token is not provided.",
            "dest": "provision_secret",
        },
    }

    @staticmethod
    def read() -> argparse.Namespace:
        """It reads the arguments passed to the program and return the variables needed.

        Returns
        -------
        argparse.Namespace
            A namespace with the arguments passed to the program.
        """
        # Create the parser.
        parser = argparse.ArgumentParser(
            description="Allows to simulate an embedded device to continue working on back-end.",
            epilog="Developed by PTAI Team",
        )

        # Add the arguments.
        for argument, options in ArgumentHandler.ARGUMENTS.items():
            parser.add_argument(argument, **options)

        # Parse the arguments.
        args = parser.parse_args()

        # Log the MAC Address and Device Token.
        logger.debug("The arguments passed to the program are: %s", args)

        # Return the arguments.
        return args
