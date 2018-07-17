# triggersafe_tests

Integration Tests for triggersafe

A real time testing tool for triggersafe that will automatically inject failures.

Types of failures to simulate:

    - Delete Pods / Containers
    - Add Pods / Containers
    - Change configurations

After failure event is simulated, have a timeout, then check if the resulting state is correct.
