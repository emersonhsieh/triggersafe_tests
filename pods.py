from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

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
    return pod.status.phase

def get_pods_list(api):
    ''' Returns list of pods
    pod_list = list of pods with metadata and status
    '''
    try: 
        api_response = api.list_pod_for_all_namespaces(watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)
        
    pod_list = []

    print("List of pods:")
    for pod in api_response.items:
        print("Namespace: {} \t IP: {} \t Pod Name: {} ".format(namespace(pod), ip(pod), name(pod)))
        pod_list.append(pod)
    
    print("\n\n")

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
    
    print("Deleted pod {}".format(name(pod)))

def delete_pod_name(api, pod_name, pod_namespace):
    ''' Delete pod without deleting deployment '''
    body = client.V1DeleteOptions()
    grace_period_seconds = 0

    try: 
        api_response = api.delete_namespaced_pod(pod_name, pod_namespace, body, grace_period_seconds=grace_period_seconds)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    
    print("Deleted pod {}".format(pod_name))
