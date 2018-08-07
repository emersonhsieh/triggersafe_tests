from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

def name(deployment):
    ''' Return name from deployment object '''
    return deployment.metadata.name

def namespace(deployment):
    ''' Return namespace from deployment object'''
    return deployment.metadata.namespace

def get_deployments(api):
    ''' Gets the list of deployments '''
    try: 
        api_response = api.list_deployment_for_all_namespaces(watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_deployment: %s\n" % e)

    deployment_list = []

    print("List of deployments:")
    for deployment in api_response.items:
        print("Namespace: {} \t Deployment Name: {} ".format(namespace(deployment), name(deployment)))
        deployment_list.append(deployment)

    print("\n\n")

    return deployment_list

def create_deployment(api, deployment_manifest, deployment_namespace):
    try: 
        api_response = api.create_namespaced_deployment(body=deployment_manifest, namespace=deployment_namespace)
    except ApiException as e:
        print("Exception when calling ExtensionsV1beta1Api->create_namespaced_deployment: %s\n" % e)

def delete_deployment(api, deployment):
    ''' Delete deployment '''
    body = client.V1DeleteOptions()
    grace_period_seconds = 0

    try: 
        api_response = api.delete_namespaced_deployment(name(deployment), namespace(deployment), body, grace_period_seconds=grace_period_seconds)
    except ApiException as e:
        print("Exception when calling ExtensionsV1beta1Api->delete_namespaced_deployment: %s\n" % e)
    
    print("Deleted deployment {}".format(name(deployment)))

def test_create_deployment(api, manifest, namespace):
    ''' Test create a deployment '''
    
    before_creation = len(get_deployments(api))
    print("Before creation: {} deployments".format(before_creation))
    create_deployment(api, manifest, namespace)
    max_attempts = 10
    cur_attempts = 0
    deployment_created = False

    while cur_attempts < max_attempts and (not deployment_created) :
        print("Checking for deployment creation, attempt {}".format(cur_attempts))
        print("Sleeping for 10 seconds...\n")
        sleep(10)

        cur_count = len(get_deployments(api))
        print("\nThere are currently {} deployments".format(cur_count))
        if cur_count > before_creation:
            print("deployment have been created")
            deployment_created = True
        cur_attempts += 1

    if deployment_created:
        print("Cooldown for newly created deployment for 10 seconds...")
        sleep(10)
        return True
    else:
        print("Deployment fails to be created")
        return False
