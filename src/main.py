import typer
import re
from podExec import *

app = typer.Typer()

@app.command()
def getinfo():
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    deviceList=execPods()
    ret = core_v1.list_namespaced_pod("default")
    for i in ret.items:
        if (i.metadata.annotations is not None):
            anno = i.metadata.annotations.get('k8s.v1.cni.cncf.io/networks-status')
            if (anno):
                l = re.findall('\w*:\w*:\w*:\w*:\w*:\w*', str(anno))
                for addr in l:
                    #print(addr)
                    for device in deviceList:
                        for vf in device.vfs:
                            if addr==str(vf.macAddress):
                                print("pod {podName} use device {deviceName} with mac address {pfMac} with vf {vfMac} in node {host}"
                                      .format(
                                    podName=i.metadata.name,
                                    deviceName=device.name,
                                    pfMac=device.macAddress,
                                    vfMac=vf.macAddress,
                                    host=device.hostName
                                ))

@app.command()
def getpods():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default")
    getIplink(v1)
    for i in ret.items:
        print(i.metadata.name)

# @app.command()
# def test():
#     getPod()



if __name__ == '__main__':
    app()
