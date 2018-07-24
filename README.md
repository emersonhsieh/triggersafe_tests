# TriggerSafe Integration Tests

A real time testing tool for triggersafe that will automatically inject failures.

This script uses the Kubernetes Python client and is tested with Python 3.7.

Types of failures to simulate:

* Delete Pods without deleting deployment (done)
* Deleting Pods with deleting deployment (done, requires testing)
* Add Pods
* Change configurations

`test_delete_pod.py` deletes all pods in the `default` namespace and checks if the pods recover upon deletion, one-by-one. Run this script using:

    python3 test_delete_pod.py

`test_delete_deployment` deletes all deployments and services in the `default` namespace and checks if all pods within the `default` namespace have been deleted. Run this script using:

    python3 test_delete_deployment.py
