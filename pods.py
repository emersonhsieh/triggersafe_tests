from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

def name(pod):
    ''' Return name from pod object '''
    return pod.metadata.name

def namespace(pod):
    ''' Return namespace from pod object'''
    return pod.metadata.namespace

def ip(pod):
    ''' Return IP from pod object'''
    return pod.status.pod_ip

def phase(pod):
    ''' Return current phase of pod object '''
    return pod.status.phase

def tier(pod):
    ''' Return tier. frontend, backend, node '''
    return pod.metadata.labels['tier']

def node(pod):
    ''' Return the node that the pod is residing on '''
    return pod.spec.node_name

def get_pods_list(api, display_pods=False):
    ''' Returns list of pods
    pod_list = list of pods with metadata and status
    '''
    try: 
        api_response = api.list_pod_for_all_namespaces(watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)
        
    pod_list = []

    if display_pods:
        print("List of pods:")
        
    for pod in api_response.items:
        if display_pods:
            print("Namespace: {} \t IP: {} \t Pod Node: {} \t\t Pod Name: {}".format(namespace(pod), ip(pod), node(pod), name(pod)))
        # print(pod)
        pod_list.append(pod)
    
    # print("\n\n")

    return pod_list

def pod_names(pods_list):
    names = []
    for pod in pods_list:
        names.append(name(pod))
    
    return names

def get_pod_by_name(pod_name, pods_list):
    for pod in pods_list:
        if name(pod) == pod_name:
            return pod

def get_containers(pod):
    ''' For debugging purposes: Get the list of containers in a pod '''
    num_containers = len(pod.status.container_statuses)
    container_ids = []
    for i in range(0, num_containers):
        container_id = pod.status.container_statuses[i].container_id
        container_ids.append(container_id)
        print("Containers: {}".format(container_id))

    return container_ids

def create_pod(api, pod_manifest, pod_namespace):
    try: 
        api_response = api.create_namespaced_pod(body=pod_manifest, namespace=pod_namespace)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

def delete_pod(api, pod):
    ''' Delete pod without deleting deployment '''
    body = client.V1DeleteOptions()
    grace_period_seconds = 0

    try: 
        api_response = api.delete_namespaced_pod(name(pod), namespace(pod), body, grace_period_seconds=grace_period_seconds)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    
    print("Delete pod {}".format(name(pod)))

def delete_pod_name(api, pod_name, pod_namespace):
    ''' Delete pod without deleting deployment '''
    body = client.V1DeleteOptions()
    grace_period_seconds = 0

    try: 
        api_response = api.delete_namespaced_pod(pod_name, pod_namespace, body, grace_period_seconds=grace_period_seconds)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    
    print("Deleted pod {}".format(pod_name))
    
def test_create_pods(api, manifest, namespace):
    ''' Test create a pod '''
    
    before_creation = len(get_pods_list(api))
    print("\n\nBefore creation: {} pods".format(before_creation))
    create_pod(api, manifest, namespace)
    max_attempts = 10
    cur_attempts = 0
    pod_created = False

    while cur_attempts < max_attempts and (not pod_created) :
        print("Checking for pod creation, attempt {}".format(cur_attempts))
        print("Sleeping for 2 seconds...\n")
        sleep(2)

        cur_count = len(get_pods_list(api))
        print("\nThere are currently {} pods".format(cur_count))
        if cur_count > before_creation:
            print("pod have been created")
            pod_created = True
        cur_attempts += 1

    if pod_created:
        print("Cooldown for newly created pod for 2 seconds...")
        sleep(2)
        return True
    else:
        print("pod fails to be created")
        return False

def exec_command(api, name, command, display_output):
    ''' Execute single command '''
    try:
        response = stream(api.connect_get_namespaced_pod_exec, name, 'default', command=command, stderr=True, stdin=False,stdout=True, tty=False)
        if display_output:
            print(response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s\n" % e)

def exec_commands(api, name, commands, display_output=False):
    ''' Execute list of commands. Use this abstraction instead of exec_command. '''
    for command in commands:
        print("Pod: {} Command: {}".format(name, command))
        command = [
            "/bin/sh",
            "-c",
            command
        ]
        exec_command(api, name, command, display_output)
