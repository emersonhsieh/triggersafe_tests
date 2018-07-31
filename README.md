# TriggerSafe Integration Tests

A real time testing tool for triggersafe that will automatically inject failures. This script uses the Kubernetes Python client and is tested with Python 3.7.

## Actions and Responses

Delete Pods without deleting deployment and services (done)

* The deleted pod is terminated, while another pod is created in its place.

Deleting Pods with deleting deployment and services (done)

* The pod is deleted and no new pods are created.

Action performed by trigger

* Respond accordingly

## Instructions

`test_create` takes in a yaml configuration, creates all the services and deployments specified in the yaml, and then tests to see if the services and deployments have been created. Run this script using:

    python3 -i test_create.py --yaml_path guestbook.yaml

`test_delete_pods.py` deletes all pods in the `default` namespace and checks if the pods recover upon deletion, one-by-one. Run this script using:

    python3 test_delete_pods.py

`test_delete_deployments` deletes all deployments and services in the `default` namespace and checks if all pods within the `default` namespace have been deleted. Run this script using:

    python3 test_delete_deployments.py
