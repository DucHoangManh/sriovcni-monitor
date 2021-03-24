class PfInfo:
    def __init__(self, name, macAddress, type, mtu, hostName):
        self.name = name
        self.macAddress = macAddress
        self.type = type
        self.mtu = mtu
        self.hostName = hostName
    def __repr__(self):
        return self.name +" "+ self.macAddress +" "+self.hostName