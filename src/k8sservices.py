from kubernetes.stream import stream
from splitString import split

def getIplink(api_instance, name):

    # Calling exec and waiting for response
    exec_command = [
        '/bin/sh',
        '-c',
        'ip link show']
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  'default',
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    iplink = resp
    # Calling exec interactively
    exec_command = ['/bin/sh']
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  'default',
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)
    resp.write_stdin("hostname\n")
    host = resp.readline_stdout(timeout=1)
    resp.close()

    return split(iplink, host)