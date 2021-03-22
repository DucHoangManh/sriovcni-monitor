from kubernetes.client.rest import ApiException
from kubernetes import client, config
from k8sservices import *
from os import path
import yaml
import time

def execPods():
    resp = None
    config.load_kube_config()
    corev1 = client.CoreV1Api()
    appv1 = client.AppsV1Api()
    try:
        resp = appv1.read_namespaced_daemon_set(name='sriov-monitor-daemonset', namespace='default')
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        print('Daemonset does not exist, creating it... ')
        with open(path.join(path.dirname(__file__), "daemonset.yaml")) as f:
            dep = yaml.safe_load(f)
            create_resp = appv1.create_namespaced_daemon_set(
                body=dep, namespace="default")
            print("Daemonset created. status='%s'" % create_resp.metadata.name)

        while True:
            resp = appv1.read_namespaced_daemon_set(name='sriov-monitor-daemonset', namespace='default')
            if (resp.status.current_number_scheduled==resp.status.desired_number_scheduled):
                break
            time.sleep(1)
        print("Daemonset created")

    resp = corev1.list_namespaced_pod(namespace='default', label_selector='name=sriov-monitor-agent', watch=False)
    result=[]
    for pod in resp.items:
        result += getIplink(corev1,pod.metadata.name)
    return result

