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
    ''' Returns list of pods
    pod_list = list of pods with metadata and status
    '''
    try: 
        api_response = api.list_pod_for_all_namespaces(watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)
        
    pod_list = []

    for pod in api_response.items:
        print("Namespace: {} \t IP: {} \t Pod Name: {} ".format(namespace(pod), ip(pod), name(pod)))
        pod_list.append(pod)

    return pod_list