# TriggerSafe Integration Tests

A testing tool for triggersafe that will automatically inject events. This script uses the Kubernetes Python client and is tested with Python 3.7.

## Instructions

`test_create.py` takes in a yaml configuration, creates all the services and deployments specified in the yaml, and then tests to see if the services and deployments have been created.

    python3 test_create.py --yaml_path <guestbook.yaml>

`test_delete_pods.py` deletes all pods in the `default` namespace and checks if the pods recover upon deletion, one-by-one.

    python3 test_delete_pods.py

`test_delete_deployments` deletes all deployments, services, and pods in the `default` namespace, then verifies that all pods within the `default` namespace do not recover.

    python3 test_delete_deployments.py

`test_autoscaling.py` creates a new pod called `request-pod`, from which requests are sent to all other frontend pods one-by-one. When running the script a second time, the script deletes and re-creates the request pod. `--request_pod_yaml` specifies the yaml configuration of the request pod. As a reference, 1000 simultaneous connections with 200,000 requests will increase both the user and system CPU usage by around 0.1%.

    python3 test_autoscaling.py --requests <amount of requests> --request_pod_yaml <ubuntu_pod.yaml>
