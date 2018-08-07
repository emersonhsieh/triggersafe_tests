from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

import pods as pods

def test_delete_pod(api, pod):
    ''' Test delete a pod
    returns True if pod recovery a success.
    returns False if pod recovery a failure.
    '''

    print("\nTest deleting: Pod Name: {} \t Pod Namespace: {}".format(pods.name(pod), pods.namespace(pod)))

    pods_before_deletion = len(pods.get_pods_list(api))
    print("Before deletion: {} pods".format(pods_before_deletion))
    
    pods.delete_pod(api, pod)
    pods_after_deletion = len(pods.get_pods_list(api))
    print("After deletion: {} pods".format(pods_after_deletion))
    
    max_attempts = 10
    cur_attempts = 0
    pod_recovers = False

    while cur_attempts < max_attempts and (not pod_recovers) :
        print("Checking for pod deletion and recovery, attempt {}".format(cur_attempts))
        print("Sleeping for 10 seconds...\n")
        sleep(10)

        cur_pod_count = len(pods.get_pods_list(api))
        print("\nThere are currently {} pods".format(cur_pod_count))

        if cur_pod_count == pods_before_deletion:
            print("Pod has been deleted and recovered!")
            pod_recovers = True

        cur_attempts += 1

    if pod_recovers:
        print("Cooldown for newly recovered pod for 10 seconds...")
        sleep(10)
        return True
    else:
        print("Pod fails to recover")
        return False
    
if __name__ == "__main__":

    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()

    # List of pods in a python list
    pods_list = pods.get_pods_list(api, display_pods=True)
    summary = []

    # Test delete pods
    # pods_list is not updated to ensure that we only delete original pods, not recovered pods
    for pod in pods_list:
        if pods.namespace(pod) == 'default':
            pod_recovered = test_delete_pod(api, pod)
            summary.append({'name': pods.name(pod),
                            'namespace': pods.namespace(pod),
                            'recovery': pod_recovered})
    
    # Print summary
    print("\n\n\n Summary:")
    for i in summary:
        print("Pod Namespace: {} \t Pod Recovered: {} \t Pod Name: {} \t ".format(i['namespace'], i['recovery'], i['name']))

