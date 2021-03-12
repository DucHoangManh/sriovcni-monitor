import typer
from k8sservices import *
from kubernetes import client, config
app = typer.Typer()

@app.command()
def getinfo():
    config.load_kube_config()

    core_v1 = client.CoreV1Api()
    deviceList=exec_commands(core_v1)
    ret = core_v1.list_namespaced_pod("default")
    for i in ret.items:
        if (i.metadata.annotations is not None):
            anno = i.metadata.annotations.get('k8s.v1.cni.cncf.io/networks-status')
            if (anno):
                l = re.findall('\w*:\w*:\w*:\w*:\w*:\w*', str(anno))
                for addr in l:
                    #print(addr)
                    for device in deviceList:
                        #print(device.macAddress)
                        if addr==str(device.macAddress):
                            print("pod {podName} use device {deviceName} with mac address {macAddr}"
                                  .format(podName=i.metadata.name, deviceName=device.name, macAddr=device.macAddress))

@app.command()
def getpods():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default")
    for i in ret.items:
        # print(i.metadata.name)
        # if hasattr(i.metadata.annotations, 'k8s.v1.cni.cncf.io/networks-status'):
        #     print(i.metadata.annotations['k8s.v1.cni.cncf.io/networks-status'])
        if (i.metadata.annotations is not None):
            anno = i.metadata.annotations.get('k8s.v1.cni.cncf.io/networks-status')
            if (anno):
                print(anno)




if __name__ == '__main__':
    app()
