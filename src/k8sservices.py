import time
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

import re
from netInfo import NetInfo

def exec_commands(api_instance):
  name = 'busybox-test'
  resp = None
  try:
    resp = api_instance.read_namespaced_pod(name=name,
                                            namespace='default')
  except ApiException as e:
    if e.status != 404:
      print("Unknown error: %s" % e)
      exit(1)

  if not resp:
    print("Pod %s does not exist. Creating it..." % name)
    pod_manifest = {
      'apiVersion': 'v1',
      'kind': 'Pod',
      'metadata': {
        'name': name
      },
      'spec': {
        'containers': [{
          'image': 'busybox',
          'name': 'sleep',
          "args": [
            "/bin/sh",
            "-c",
            "while true;do date;sleep 5; done"
          ]
        }],
        'hostNetwork': True,
        'imagePullPolicy': 'Never',
        'imagePullSecrets': [{
          'name': 'regcred'
        }]
      }
    }
    resp = api_instance.create_namespaced_pod(body=pod_manifest,
                                              namespace='default')
    while True:
      resp = api_instance.read_namespaced_pod(name=name,
                                              namespace='default')
      if resp.status.phase != 'Pending':
        break
      time.sleep(1)
    print("Done.")

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
  l = re.findall('\d+:\s.+\s{4}.+', resp)


  # Calling exec interactively
  exec_command = ['/bin/sh']
  resp = stream(api_instance.connect_get_namespaced_pod_exec,
                name,
                'default',
                command=exec_command,
                stderr=True, stdin=True,
                stdout=True, tty=False,
                _preload_content=False)
  commands = [
    #        "ip link show"
  ]

  while resp.is_open():
    resp.update(timeout=1)
    if resp.peek_stdout():
      print("STDOUT: %s" % resp.read_stdout())
    if resp.peek_stderr():
      print("STDERR: %s" % resp.read_stderr())
    if commands:
      c = commands.pop(0)
      print("Running command... %s\n" % c)
      resp.write_stdin(c + "\n")
    else:
      break

  resp.write_stdin("hostname\n")
  host = resp.readline_stdout(timeout=1)
  resp.close()

  result = []
  for item in l:
    _item = item.split(' ')
    if (_item[1] == "lo:"):
      continue
    n = NetInfo(
      name=_item[1],
      macAddress=_item[14],
      type=_item[2],
      mtu=_item[4],
      hostName=host
    )
    result.append(n)
  return result
