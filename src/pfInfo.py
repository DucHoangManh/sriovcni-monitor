class PfInfo:
    def __init__(self, name, macAddress, type, mtu, vfs, hostName):
        self.name = name
        self.macAddress = macAddress
        self.type = type
        self.mtu = mtu
        self.vfs = vfs
        self.hostName = hostName
    def __repr__(self):
        return self.name +" "+ self.macAddress +" "+self.hostName