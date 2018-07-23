from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

import argparse
from time import sleep
from subprocess import call

import pods as pods

def get_services(api, namespace):
    ''' Debug purposes: Gets the list of services
    To get the name of the service: api_response.items[0].metadata.name
    '''
    
    try: 
        api_response = api.list_namespaced_service(namespace, watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)

    return api_response
    
def check_default_namespace():
    ''' Checks that there are no pods left within the 'default' namespace. '''
    
    max_attempts = 10
    cur_attempts = 0
    no_pods_in_default = False

    while cur_attempts < max_attempts and (not no_pods_in_default):
        print("Checking that there are no pods in default namespace, attempt {}".format(cur_attempts))
        print("Sleeping for 5 seconds...\n")
        sleep(5)

        pods_list = pods.get_pods_list(api)
        
        # Assume false until a pod in 'default' is found.
        pod_in_default = False

        for pod in pods_list:
            if pods.namespace(pod) == 'default':
                pod_in_default = True
        
        if (not pod_in_default):
            no_pods_in_default = True
        else:
            cur_attempts += 1
    
    return no_pods_in_default

if __name__ == "__main__":
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml_path", help="Path to yaml deployment configuration")
    args = parser.parse_args()
    assert (args.yaml_path != None), "Must include path to yaml deployment configuration"

    print("Deleting deployment...")
    deletion_command = "kubectl delete -f {}".format(args.yaml_path)
    
    call(deletion_command, shell=True)
    print("Pods Deleted")
    
    pods_deleted = check_default_namespace()
    if pods_deleted:
        print("All pods in default namespace successfully deleted")
    else:
        print("Deployment deletion not successful")
