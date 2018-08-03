from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

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
        "ab -k -c 350 -n 2000000 localhost:80/",
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
    

if __name__ == "__main__":
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()
    apps_api = client.AppsV1beta1Api()
    
    pods_list = pods.get_pods_list(api)
    
    # Test on first pod
    pods.get_containers(pods_list[0])
    increase_load(api, pods.name(pods_list[0]), 0.2)

    pods_list_new = pods.get_pods_list(api)
    
    print("Scaled from {} pods to {} pods".format(len(pods_list), len(pods_list_new)))

    if len(pods_list_new) == 1 + len(pods_list):
        print("Success")
    else:
        print("Fail")
        
