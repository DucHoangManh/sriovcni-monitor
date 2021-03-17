import re
from pfInfo import PfInfo
from vfInfo import VfInfo

def split(str, hostName):
    pattern = re.compile('\d: .*\s*.*\s*(?:vf.*\s*)+')
    macPattern = re.compile('\w*:\w*:\w*:\w*:\w*:\w*')
    vfPattern = re.compile('vf.*')
    pfList = pattern.findall(str)
    pfs=[]
    for pf in pfList:
        vfList = vfPattern.findall(pf)
        vfs=[]
        for vf in vfList:
            _vf = vf.split(' ')
            v = VfInfo(
                index=_vf[1],
                macAddress=macPattern.search(vf).group()
            )
            vfs.append(v)
        _pf = pf.split(' ')
        p = PfInfo(
            name=_pf[1],
            type=_pf[2],
            hostName=hostName,
            mtu=_pf[4],
            macAddress=_pf[19],
            vfs=vfs
        )
        pfs.append(p)
    return pfs

