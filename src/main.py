import typer
from src.k8sservices import *

app = typer.Typer()

@app.command()
def getinfo():
    config.load_kube_config()
    # c = Configuration()
    # c.assert_hostname = False
    # Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    exec_commands(core_v1)

@app.command()
def getpods():
    config.load_kube_config()
    api = core_v1_api.CoreV1Api()
    resp = api.list_namespaced_pod("default")
    for i in resp.items:
        print(i.metadata.annotations)

if __name__ == '__main__':
    app()
