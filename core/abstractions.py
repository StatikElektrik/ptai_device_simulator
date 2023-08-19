"""
This module contains the abstractions of the device to simulate its behaviour.
"""

import logging

# Create a logger interface.
logger = logging.getLogger(__name__)


class Modem:
    """This class represents the modem of the device."""

    def __init__(self, imei: str = "FFFFFFFFFFFFFFFF", fw_ver: str = "0"):
        self.imei = imei
        self.fw_ver = fw_ver


class SimCard:
    """This class represents the SIM card of the device."""

    def __init__(self, iccid: str = "FFFFFFFFFFFFFFFFFFFF", imsi: str = "FFFFFFFFFFF"):
        self.iccid = iccid
        self.imsi = imsi


class Device:
    """This class represents the device to be simulated."""

    def __init__(
        self,
        mac_address: str,
        firmware: str = "0.0.1",
    ):
        self.is_registered = False
        self.mac_address = mac_address
        self.fw_version = firmware

        self._provision_key: str
        self._provision_secret: str
        self._token: str

        # Not used for now.
        # self.state = 0
        # self.error = 0
        # self._modem = Modem()
        # self._sim_card = SimCard()

    def set_provision_key(self, provision_key: str) -> None:
        """It sets the provision key of the device."""
        self._provision_key = provision_key

    def set_provision_secret(self, provision_secret: str) -> None:
        """It sets the provision secret of the device."""
        self._provision_secret = provision_secret

    def set_token(self, token: str) -> None:
        """It sets the token of the device."""
        self._token = token
        self.is_registered = True

    def get_provision_info(self) -> tuple:
        """It returns the provision info of the device."""
        if self.is_registered:
            raise UserWarning("The device is already registered.")

        # Check if the provision key and secret are set.
        if not self._provision_key or not self._provision_secret:
            raise ValueError("The provision key and secret are not set.")

        return self._provision_key, self._provision_secret

    def get_token(self) -> str:
        """It returns the token of the device."""
        if not self.is_registered:
            raise UserWarning("The device is not registered.")

        return self._token

    def to_dict(self):
        """It returns a dictionary with the device information."""
        return {
            # "state": self.state,
            # "error": self.error,
            "fw": self.fw_version,
            "is_registered": self.is_registered,
            # "IMEI": self.modem.imei,
            # "modem_fw": self.modem.fw_ver,
            # "ICCID": self.sim_card.iccid,
            # "IMSI": self.sim_card.imsi,
        }
     
    @staticmethod
    def create_formatted_data_pool(*args):
        """
        Given the error types and the values of errors, return a formatted dictionary.

        Parameters
        ----------
        *args : list or str
            Expected data format : 'error_type_name', [list], 'error_type_name_2', [list] ....

        Returns
        -------
        dict
            Return the given data with the format that is expected by the device.
            Example: {'e1': [10,20,30,40], 'e2': [20,30,40,50]}
        """
        data_pool = {}
        for i in range(0, len(args), 2):
            entity = args[i]
            value = args[i + 1]
            data_pool[entity] = value
        return data_pool
