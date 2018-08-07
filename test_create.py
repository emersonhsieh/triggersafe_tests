from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

import argparse

from time import sleep
import yaml as yaml
import pods as pods
import services
import deployments
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml_path", help="Path to yaml deployment configuration")
    args = parser.parse_args()
    assert (args.yaml_path != None), "Must include path to yaml deployment configuration"
    
    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()
    apps_api = client.AppsV1beta1Api()

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
            creation = deployments.test_create_deployment(apps_api, manifest=manifest, namespace='default')
        elif kind == 'Service':
            creation = services.test_create_service(api, manifest=manifest, namespace='default')
        
        summary.append({'kind': kind,
                        'name': name,
                        'namespace': namespace,
                        'creation': creation})

    # Print summary
    print("\n\n\n Summary:")
    for i in summary:
        print("Kind: {} \t\t Creation Success: {} \t Namespace: {}  \t Name: {}".format(i['kind'], i['creation'], i['namespace'], i['name']))
