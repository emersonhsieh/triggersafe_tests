from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

def pod_name(pod):
    ''' Return name from pod object '''
    return pod.metadata.name

def pod_namespace(pod):
    ''' Return namespace from pod object'''
    return pod.metadata.namespace

def get_pods_list(api):
    '''
    Returns list of pods
    pod_list = list of pods with matadata and status
    '''
    ret = api.list_pod_for_all_namespaces(watch=False)
    pod_list = []

    for i in ret.items:
        print("Pod IP: {} \t Namespace: {} \t Name: {}".format(i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        pod_list.append(i)

    return pod_list

def delete_pod(api, pod):
    ''' Delete pod without deleting deployment '''

    name = pod_name(pod)
    namespace = pod_namespace(pod)
    body = client.V1DeleteOptions()
    pretty = 'Pod deleted successfully'
    grace_period_seconds = 0
    propagation_policy = 'propagation_policy_example'

    try: 
        api_response = api.delete_namespaced_pod(name, namespace, body, pretty=pretty, grace_period_seconds=grace_period_seconds, propagation_policy=propagation_policy)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    
    print("Deleted pod {}".format(name))

def get_containers(pod):
    num_containers = len(pod.status.container_statuses)

    container_ids = []
    for i in range(0, num_containers):
        container_ids.append(pods_list[pod_index].status.container_statuses[i].container_id)

    return container_ids

def test_delete_pod(api, pod):
    print("Test delete pod")
    print("Name: {} Namespace: {}".format(pod_name(pod), pod_namespace(pod)))

    pods_before_deletion = len(get_pods_list(api))
    print("Before deletion: {} pods".format(pods_before_deletion))
    
    delete_pod(api, pod)
    pods_after_deletion = len(get_pods_list(api))
    print("After deletion: {} pods".format(pods_after_deletion))
    
    max_attempts = 10
    cur_attempts = 0
    pod_recovers = False

    while cur_attempts < max_attempts and (not pod_recovers) :
        print("Checking for pod recovery, attempt {}".format(cur_attempts))
        print("Sleeping for 5 seconds...")
        sleep(5)

        cur_pod_count = len(get_pods_list(api))
        print("\nThere are currently {} pods".format(cur_pod_count))

        if cur_pod_count == pods_before_deletion:
            print("Container has recovered!")
            pod_recovers = True

        cur_attempts += 1

    if pod_recovers:
        print("Pod recover successfully")
    else:
        print("Pod fails to recover")
    
    print("Cooldown for newly created pod for 20 seconds...")
    sleep(20)

if __name__ == "__main__":

    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()

    # List of pods in a python list
    pods_list = get_pods_list(api)

    # Deleting a pod:
    # Testing deleting a pod
    for pod in pods_list:
        if pod_namespace(pod) == 'default':
            test_delete_pod(api, pod)

