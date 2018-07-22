from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

def name(pod):
    ''' Return name from pod object '''
    return pod.metadata.name

def namespace(pod):
    ''' Return namespace from pod object'''
    return pod.metadata.namespace

def get_pods_list(api):
    '''
    Returns list of pods
    pod_list = list of pods with metadata and status
    '''
    ret = api.list_pod_for_all_namespaces(watch=False)
    pod_list = []

    for i in ret.items:
        print("Pod IP: {} \t Namespace: {} \t Name: {}".format(i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        pod_list.append(i)

    return pod_list