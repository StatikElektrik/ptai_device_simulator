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
    def __init__(self, name: str, fw_version: str, provision_key: str, provision_secret: str):
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

    def set_token(self, token: str) -> None:
        """It sets the token of the device."""
        self.token = token
        self.is_registered = True

    def to_dict(self):
        """It returns a dictionary with the device information."""
        return {
            "state": self.state,
            "error": self.error,
            "fw": self.fw_version,
            "is_registered": self.is_registered,
            "IMEI": self.modem.imei,
            "modem_fw": self.modem.fw_ver,
            "ICCID": self.sim_card.iccid,
            "IMSI": self.sim_card.imsi,
        }
