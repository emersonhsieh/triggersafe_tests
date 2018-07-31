from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

import argparse

from time import sleep
import yaml as yaml
import pods as pods
import services
import deployments

def test_create_service(api, manifest, namespace):
    ''' Test create a service '''
    
    before_creation = len(services.get_services(api))
    print("Before creation: {} services".format(before_creation))
    services.create_service(api, manifest, namespace)
    max_attempts = 10
    cur_attempts = 0
    service_created = False

    while cur_attempts < max_attempts and (not service_created) :
        print("Checking for service creation, attempt {}".format(cur_attempts))
        print("Sleeping for 10 seconds...\n")
        sleep(10)

        cur_count = len(services.get_services(api))
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

def test_create_deployment(api, manifest, namespace):
    ''' Test create a deployment '''
    
    before_creation = len(deployments.get_deployments(api))
    print("Before creation: {} deployments".format(before_creation))
    deployments.create_deployment(api, manifest, namespace)
    max_attempts = 10
    cur_attempts = 0
    deployment_created = False

    while cur_attempts < max_attempts and (not deployment_created) :
        print("Checking for deployment creation, attempt {}".format(cur_attempts))
        print("Sleeping for 10 seconds...\n")
        sleep(10)

        cur_count = len(deployments.get_deployments(api))
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
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml_path", help="Path to yaml deployment configuration")
    args = parser.parse_args()
    assert (args.yaml_path != None), "Must include path to yaml deployment configuration"
    
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()

    # Change filename to location of yaml config
    stream = open(args.yaml_path, 'r')
    manifests = yaml.load_all(stream)

    summary = []

    for manifest in manifests:

        print(manifest)
        kind = manifest['kind']
        name = manifest['metadata']['name']
        namespace = 'default'
        
        if kind == 'Deployment':
            creation = test_create_deployment(beta_api, manifest=manifest, namespace='default')
        elif kind == 'Service':
            creation = test_create_service(api, manifest=manifest, namespace='default')
        
        summary.append({'kind': kind,
                        'name': name,
                        'namespace': namespace,
                        'creation': creation})

    # Print summary
    print("\n\n\n Summary:")
    for i in summary:
        print("Kind: {} \t Namespace: {} \t Name: {} \t Creation Success: {} \t ".format(i['kind'], i['namespace'], i['creation'], i['name']))
