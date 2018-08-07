from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep
import argparse
import yaml as yaml

import pods as pods

def increase_load(api, request_pod_name, stress_pod, load_amount):
    stress_pod_name = pods.name(stress_pod)
    stress_pod_ip = pods.ip(stress_pod)

    ab_command = "ab -k -c 1000 -n " + str(load_amount) + " " + stress_pod_ip + ":80/"

    # First, get mpstat of stress_pod
    # If there is an apt-get error, add the display_output=True to exec_commands
    print("\n\nGetting mpstat of pod being stressed")
    install_sysstat = [
        "apt-get update",
        "apt-get -y install sysstat",
    ]
    pods.exec_commands(api, stress_pod_name, install_sysstat)

    # View CPU usage
    pods.exec_commands(api, stress_pod_name, ["mpstat"], display_output=True)

    # Stressing remotely.
    print("\n\nStressing pod remotely")
    commands = [
        "apt-get update",
        "apt-get -y install apache2-utils"
    ]
    pods.exec_commands(api, request_pod_name, commands)
    pods.exec_commands(api, request_pod_name, [ab_command], display_output=True)
    print("\n\nPod stressed")

    # Then, get mpstat of stress_pod to see cpu usage.
    print("\n\nGetting mpstat again of pod being stressed")
    pods.exec_commands(api, stress_pod_name, ["mpstat"], display_output=True)

def create_request_pod(api, request_pod_name, request_pod_manifest):
    pods_list = pods.get_pods_list(api)
    pods_names = pods.pod_names(pods_list)

    # First delete an existing pod if it exists
    if request_pod_name in pods_names:
        pods.delete_pod_name(api, request_pod_name, 'default')
        print("Wait for existing request pod to terminate...")

        request_pod_terminated = False
        while not request_pod_terminated:
            pods_list_new = pods.get_pods_list(api)
            pods_names_new = pods.pod_names(pods_list_new)

            print("Checking if pod terminated")
            if request_pod_name in pods_names_new:
                sleep(5)
            else:
                request_pod_terminated = True
                print("Existing request pod terminated.")
    
    # Creating request pod
    pods.create_pod(api, request_pod_manifest, 'default')
    print("Creating request pod:")
    
    request_pod_created = False
    while not request_pod_created:
        pods_list_new = pods.get_pods_list(api)
        pods_names_new = pods.pod_names(pods_list_new)

        print("Checking if pod is in list of pods")
        if request_pod_name in pods_names_new:
            request_pod_created = True
            print("Request pod created")
        else:
            sleep(5)

    # Check if request pod is running:
    request_pod = pods.get_pod_by_name(request_pod_name, pods_list_new)
    print("Check if request pod is running:")
    
    request_pod_running = False
    while not request_pod_created:
        print("Request pod at phase: {}".format(pods.phase(request_pod)))
        if pods.phase(request_pod) == 'Running':
            request_pod_running = True
        else:
            sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", help="Number of requests")
    parser.add_argument("--request_pod_yaml", help="Request pod yaml configuration")
    args = parser.parse_args()
    assert (args.requests != None), "Must include the number of requests: recommended 2000000"
    assert (args.request_pod_yaml != None), "Must include the yaml for the request pod"
    
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()
    apps_api = client.AppsV1beta1Api()

    # Request pod information
    yaml_stream = open(args.request_pod_yaml, 'r')
    manifests = yaml.load_all(yaml_stream)
    
    request_pod_manifest = next(manifests)
    request_pod_name = request_pod_manifest['metadata']['name']

    create_request_pod(api, request_pod_name, request_pod_manifest)

    pods_list = pods.get_pods_list(api)
    
    for stress_pod in pods_list:
        if pods.namespace(stress_pod) == 'default' and pods.tier(stress_pod) == 'frontend':
            print('*' * 60)
            increase_load(api, request_pod_name, stress_pod, int(args.requests))

    # Check if autoscaled

    pods_list_new = pods.get_pods_list(api)

    print("Scaled from {} pods to {} pods".format(len(pods_list), len(pods_list_new)))

