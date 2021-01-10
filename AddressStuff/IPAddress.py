
class IPAddress:
    def __init__(self, _ip):
        self.ip = _ip
        self.mac = ""
        self.free = True
        self.keep = False


    def setMac(self, _mac):
        self.mac = _mac

    def set_IP_unavailable(self):
        """Se seteaza ca adresa IP sa nu fie disponibila"""
        self.free = False

    def keep_IP_address(self):
        """Se seteaza ca adresa IP sa fie retinuta"""
        self.keep = True

    def make_IP_available(self):
        self.free = True

    def release_IP_address(self):
        self.keep = False
        self.mac = ""