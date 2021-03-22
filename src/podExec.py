from kubernetes import client, config

def getPod():
    config.load_kube_config()
    appv1 = client.AppsV1Api()
    resp = appv1.list_namespaced_daemon_set('default')
    print(resp)