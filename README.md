# TriggerSafe Integration Tests

A testing tool for triggersafe that will automatically inject events. This script uses the Kubernetes Python client and is tested with Python 3.7.

## Instructions

### Creating Services and Deployments

`test_create.py` takes in a yaml configuration, creates all the services and deployments specified in the yaml, and then tests to see if the services and deployments have been created. The script will print out a summary at the end.

    python3 test_create.py --yaml_path guestbook.yaml

### Deleting Pods

`test_delete_pods.py` deletes all pods in the `default` namespace and checks if the pods recover upon deletion, one-by-one. The script will print out a summary at the end.

    python3 test_delete_pods.py

### Deleting Deployments

`test_delete_deployments` deletes all deployments, services, and pods in the `default` namespace, then verifies that all pods within the `default` namespace do not recover.

    python3 test_delete_deployments.py

### Elastic Autoscaler

`test_autoscaling.py` creates a new pod called `request-pod`, from which requests are sent to all other `frontend` pods one-by-one. When running the script a second time, the script deletes and re-creates the request pod. The `request_pod_yaml` flag specifies the yaml configuration of the request pod. As a reference, 1000 simultaneous connections with 200,000 requests will increase both the user and system CPU usage by around 0.1%.

To use a custom request pod configuration, use a ubuntu image and make sure that the `label` is not set to `frontend`.

    python3 test_autoscaling.py --requests <amount of requests> --request_pod_yaml ubuntu_pod.yaml

The script will print a summary to compare the number of nodes before and after sending the requests.

### MovePod

`test_distribution.py` creates a specified number of nginx pods on a given node. The user will then be prompted to call the MovePod trigger, after which the script will print out the new distribution of pods on nodes.

Before running this script, the user needs to label a node with a custom label, like so:

    kubectl label nodes ip-172-20-46-211.us-west-1.compute.internal node=my_node

Use the label in the previous command for the `pods_hostname` flag. A specificied number of pods are then placed on that node.

    python3 test_distribution.py --pods_to_create <number of pods> --pods_hostname <my_node> --yaml_path nginx.yaml
