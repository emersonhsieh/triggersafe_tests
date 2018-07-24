from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

import argparse
from time import sleep
from subprocess import call

import pods as pods
import deployments as deployments
import services as services
    
def check_empty_namespace(api, namespace):
    ''' Checks that there are no pods left within a namespace. '''
    
    max_attempts = 10
    cur_attempts = 0
    no_pods_in_default = False

    while cur_attempts < max_attempts and (not no_pods_in_default):
        print("Checking that there are no pods in namespace: {}, attempt {}".format(namespace, cur_attempts))
        print("Sleeping for 5 seconds...\n")
        sleep(5)

        pods_list = pods.get_pods_list(api)
        
        # Assume false until a pod in 'default' is found.
        pod_in_default = False

        for pod in pods_list:
            if pods.namespace(pod) == namespace:
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
    beta_api = client.ExtensionsV1beta1Api()

    print("\n\n Delete all deployments in default")
    deployments_list = deployments.get_deployments(beta_api)
    for deployment in deployments_list:
        if deployments.namespace(deployment) == 'default':
            deployments.delete_deployment(beta_api, deployment)

    print("\n\n Delete all services in default")
    services_list = services.get_services(api)
    for service in services_list:
        if services.namespace(service) == 'default':
            services.delete_service(api, service)

    print("\n\n Delete all pods in default")
    pods_list = pods.get_pods_list(api)
    for pod in pods_list:
        if pods.namespace(pod) == 'default':
            pods.delete_pod(api, pod)

    pods_deleted = check_empty_namespace(api, 'default')
    if pods_deleted:
        print("All pods in default namespace successfully deleted")
    else:
        print("Deployment deletion not successful")
