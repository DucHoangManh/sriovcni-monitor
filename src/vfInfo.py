class VfInfo:
    def __init__(self, index, macAddress):
        self.index = index
        self.macAddress = macAddress
    def __repr__(self):
        return self.index +' '+ self.macAddress

