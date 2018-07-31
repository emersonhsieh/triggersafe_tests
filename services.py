from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

def name(service):
    ''' Return name from service object '''
    return service.metadata.name

def namespace(service):
    ''' Return namespace from service object'''
    return service.metadata.namespace

def get_services(api):
    ''' Gets the list of services '''
    try: 
        api_response = api.list_service_for_all_namespaces(watch=False)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_service_for_all_namespaces: %s\n" % e)

    service_list = []

    print("List of services:")
    for service in api_response.items:
        print("Namespace: {} \t Service Name: {} ".format(namespace(service), name(service)))
        service_list.append(service)

    print("\n\n")

    return service_list

def create_service(api, service_manifest, service_namespace):
    try: 
        api_response = api.create_namespaced_service(body=service_manifest, namespace=service_namespace)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)

def delete_service(api, service):
    ''' Delete service '''
    body = client.V1DeleteOptions()
    grace_period_seconds = 0

    try: 
        api_response = api.delete_namespaced_service(name(service), namespace(service), body, grace_period_seconds=grace_period_seconds)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
    
    print("Deleted service {}".format(name(service)))

