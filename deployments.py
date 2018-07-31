from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

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
