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
                        if addr==str(device.macAddress):
                            print("pod {podName} with Ip {podIp} use device {deviceName} with mac address {pfMac} in node {host}"
                                  .format(
                                podName=i.metadata.name,
                                deviceName=device.name,
                                pfMac=device.macAddress,
                                podIp=i.status.pod_ip,
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

@app.command()
def cleanup():
    config.load_kube_config()
    appsv1 = client.AppsV1Api
    api_response = appsv1.delete_namespaced_daemon_set(
        name="sriov-monitor-daemonset",
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Daemonset deleted. status='%s'" % str(api_response.status))



if __name__ == '__main__':
    app()
