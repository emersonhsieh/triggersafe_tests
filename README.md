# TriggerSafe Integration Tests

A real time testing tool for triggersafe that will automatically inject failures.

This script uses the Kubernetes Python client and runs with Python3.

Types of failures to simulate:

* Delete Pods without deleting deployment
* Deleting Pods with deleting deployment
* Add Pods
* Change configurations
