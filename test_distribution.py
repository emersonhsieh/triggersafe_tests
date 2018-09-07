from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException

from time import sleep
import argparse
import yaml as yaml

import deployments
import pods as pods

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--pods_to_create", help="number of pods to be booted")
    # parser.add_argument("--pods_hostname", help="hostname for pods")
    # parser.add_argument("--yaml_path", help="yaml for pods")
    # args = parser.parse_args()
    # assert (args.yaml_path != None), "Must include the yaml for pod creation"
    # assert (args.pods_to_create != None), "Must include the number of pods to create"
    # assert (args.pods_hostname != None), "Must include primary hostname for pods"

    # Initialize API
    config.load_kube_config()
    api = client.CoreV1Api()
    beta_api = client.ExtensionsV1beta1Api()
    apps_api = client.AppsV1beta1Api()

    # # Create services and pods
    # stream = open(args.yaml_path, 'r')
    # manifests = yaml.load_all(stream)
    #
    # summary = []
    #
    # for manifest in manifests:
    #     print(manifest)
    #     kind = manifest['kind']
    #     name = manifest['metadata']['name']
    #     namespace = 'default'
    #
    #     if kind == 'Deployment':
    #         creation = deployments.test_create_deployment(apps_api, manifest=manifest, namespace='default')
    #
    #         summary.append({'kind': kind,
    #                     'name': name,
    #                     'namespace': namespace,
    #                     'creation': creation})
    #     elif kind == 'Pod':
    #         base_name = manifest['metadata']['name']
    #         for i in range(0, int(args.pods_to_create)):
    #             manifest['metadata']['name'] = base_name + str(i)
    #             manifest['spec']['nodeSelector']['node'] = args.pods_hostname
    #             creation = pods.test_create_pods(api, manifest=manifest, namespace='default')
    #
    #             summary.append({'kind': kind,
    #                     'name': name,
    #                     'namespace': namespace,
    #                     'creation': creation})
    #
    # pods_list = pods.get_pods_list(api, display_pods=True)
    #
    #
    # # Calculate the pods per node for the created pods:
    # # key, value = node, number of pods
    # node_pod_count = {}
    #
    # for pod in pods_list:
    #     if pods.namespace(pod) == 'default':
    #         if pods.node(pod) not in node_pod_count:
    #             node_pod_count[pods.node(pod)] = 0
    #         else:
    #             node_pod_count[pods.node(pod)] += 1
    #
    # print("Current distribution:")
    # for k, v in node_pod_count.items():
    #     print("Node: {} \t Number of Pods: {}".format(k, v))
    #
    #     #TODO: LOOK INTO DELETING ABOVE, run guestbook as normal
    # Calculate the pods per node for the created pods:
    # key, value = node, number of pods

    while True:
        new_pods_list = pods.get_pods_list(api, display_pods=True)
        new_node_pod_count = {}

        for pod in new_pods_list:
            if pods.namespace(pod) == 'default':
                if pods.node(pod) not in new_node_pod_count:
                    new_node_pod_count[pods.node(pod)] = 0
                else:
                    new_node_pod_count[pods.node(pod)] += 1

        print("\n\nNew distribution:")
        for k, v in new_node_pod_count.items():
            print("Node: {} \t Number of Pods: {}".format(k, v))

        input("\n\nPress enter to continue...")
