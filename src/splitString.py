import re
from pfInfo import PfInfo

def split(str, hostName):
    #pattern = re.compile('\d: .*\s*.*\s*(?:vf.*\s*)+')
    pattern = re.compile('\d: .*\s*.*\s*')
    macPattern = re.compile('\w*:\w*:\w*:\w*:\w*:\w*')
    pfList = pattern.findall(str)
    pfs=[]
    for pf in pfList:
        _pf = pf.split(' ')
        p = PfInfo(
            name=_pf[1],
            type=_pf[2],
            hostName=hostName,
            mtu=_pf[4],
            macAddress=_pf[14],
        )
        pfs.append(p)
    return pfs

