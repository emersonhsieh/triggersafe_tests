from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep

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

def test_create_service(api, manifest, namespace):
    ''' Test create a service '''
    
    before_creation = len(get_services(api))
    print("Before creation: {} services".format(before_creation))
    create_service(api, manifest, namespace)
    max_attempts = 10
    cur_attempts = 0
    service_created = False

    while cur_attempts < max_attempts and (not service_created) :
        print("Checking for service creation, attempt {}".format(cur_attempts))
        print("Sleeping for 10 seconds...\n")
        sleep(10)

        cur_count = len(get_services(api))
        print("\nThere are currently {} services".format(cur_count))
        if cur_count > before_creation:
            print("Service have been created")
            service_created = True
        cur_attempts += 1

    if service_created:
        print("Cooldown for newly created service for 10 seconds...")
        sleep(10)
        return True
    else:
        print("Service fails to be created")
        return False
