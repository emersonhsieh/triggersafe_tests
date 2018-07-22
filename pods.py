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

def get_pods_list(api):
    '''
    Returns list of pods
    pod_list = list of pods with metadata and status
    '''
    ret = api.list_pod_for_all_namespaces(watch=False)
    pod_list = []

    for pod in ret.items:
        print("Namespace: {} \t IP: {} \t Pod Name: {} ".format(namespace(pod), ip(pod), name(pod)))
        pod_list.append(pod)

    return pod_list