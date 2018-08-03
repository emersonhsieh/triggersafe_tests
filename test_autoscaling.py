from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

import pods as pods

def exec_command(api, name, command):
    try:
        response = stream(api.connect_get_namespaced_pod_exec, name, 'default', command=command, stderr=True, stdin=False,stdout=True, tty=False)
        print(response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s\n" % e)

def increase_load(api, name, load_percentage):
    # calling exec and wait for response.
    commands = [
        "apt-get update",
        "apt-get -y install stress",
        "apt-get -y install sysstat",
        "mpstat",
        "ab -k -c 1000 -n 2000000 localhost:80/" ,
        "mpstat"
    ]
    for command in commands:
        print(command)
        command = [
            "/bin/sh",
            "-c",
            command
        ]
        exec_command(api, name, command)
    
def create_request_pod(api, request_pod_name, request_pod_manifest):
    pods_list = pods.get_pods_list(api)
    pods_names = pods.pod_names(pods_list)

    # First delete an existing pod if it exists
    if request_pod_name in pods_names:
        pods.delete_pod_name(api, request_pod_name, 'default')
        print("Wait for existing request pod to terminate...")

        request_pod_terminated = False
        while not request_pod_terminated:
            print("Checking if pod terminated")
            if request_pod_name in pods_names:
                sleep(5)
            else:
                request_pod_terminated = True
                print("Existing request pod terminated.")
    
    # Creating request pod
    pods.create_pod(api, request_pod_manifest, 'default')
    print("Creating request pod:")
    
    request_pod_created = False
    while not request_pod_created:
        print("Checking if pod is in list of pods")
        if request_pod_name in pods_names:
            request_pod_created = True
            print("Request pod created")
        else:
            sleep(5)

    # Check if request pod is running:
    request_pod = pods.get_pod_by_name(request_pod_name)
    print("Check if request pod is running:")
    
    request_pod_running = False
    while not request_pod_created:
        print("Request pod at phase: {}".format(pods.phase(request_pod)))
        if pods.phase(request_pod) == 'Running':
            request_pod_running = True
        else:
            sleep(5)

if __name__ == "__main__":
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()
    apps_api = client.AppsV1beta1Api()

    # Request pod information
    request_pod_name = 'request-pod'
    request_pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'request-pod'
        },
        'spec': {
            'containers': [{
                'image': 'ubuntu',
                'name': 'sleep',
                "args": [
                    "/bin/sh",
                    "-c",
                ]
            }]
        }
    }

    create_request_pod(api, request_pod_name, request_pod_manifest)
    
    # Test on first pod
    increase_load(api, request_pod_name, 0.2)

    pods_list_new = pods.get_pods_list(api)
    
    print("Scaled from {} pods to {} pods".format(len(pods_list), len(pods_list_new)))

    if len(pods_list_new) == 1 + len(pods_list):
        print("Success")
    else:
        print("Fail")
        
