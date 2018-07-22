# TriggerSafe Integration Tests

A real time testing tool for triggersafe that will automatically inject failures.

This script uses the Kubernetes Python client and runs with Python3.

Types of failures to simulate:

* Delete Pods without deleting deployment (done)
* Deleting Pods with deleting deployment
* Add Pods
* Change configurations

`test_delete_pod.py` deletes all pods in the `default` namespace and checks if the pods recover upon deletion, one-by-one. Run this script using:

`python3 test_delete_pod.py`