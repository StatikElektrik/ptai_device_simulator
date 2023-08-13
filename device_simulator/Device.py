import logging
logger = logging.getLogger('Device')

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
        self.is_registered = True

    def to_dict(self):
        return {
            "state": self.state,
            "error": self.error,
            "fw": self.fw_version,
            "is_registered": self.is_registered,
            "IMEI": self.modem.IMEI,
            "modem_fw": self.modem.fw_ver,
            "ICCID": self.sim_card.ICCID,
            "IMSI": self.sim_card.IMSI
        }