import subprocess
import remote_execution as remote_exec

from kubernetes import client, config
from kubernetes.stream import stream

def get_pods_list():
    '''
    Returns a dictionary of pods.
    pod_list[name] = (status, metadata).
    '''
    config.load_kube_config()

    api = client.CoreV1Api()
    ret = api.list_pod_for_all_namespaces(watch=False)

    pod_list = {}

    for i in ret.items:
        print("Pod IP: {} \t Namespace: {} \t Name: {}".format(i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        pod_list[i.metadata.name] = (status, metadata)

    return pod_list

# def get_pod_status(pod_name, pod_namespace, pod_ip):
#     pods = get_pods_list()
#     current_pod = pods[pod_name]

def exec_command(pod_name, pod_namespace, command_list):
    '''
    Executes commands in a pod.
    '''
    config.load_kube_config()    
    client_config = client.Configuration()
    client_config.assert_hostname = False
    client.Configuration.set_default(c)
    
    api = client.CoreV1Api()
    resp = stream(
            api.connect_get_namespaced_pod_exec, name, pod_namespace,
            command=exec_command,
            stderr=True, stdin=True,
            stdout=True, tty=False,
            _preload_content=False)

    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            print("STDOUT: %s" % resp.read_stdout())
            return resp.read_stdout()

        if resp.peek_stderr():
            print("STDERR: %s" % resp.read_stderr())
        if commands:
            c = commands.pop(0)
            print("Running command... %s\n" % c)
            resp.write_stdin(c + "\n")
        else:
            break

def get_containers(pod_name, pod_namespace):
    get_containers = [
        "/bin/sh",
        "docker ps",
        "docker stop {}".format(container_id)
    ]
    container_ids = exec_command(pod_name, pod_namespace, get_containers).splitlines()
    return container_ids

def test_delete_container(pod_name, pod_namespace):
    print("Testing deleting pod with name: {} and namespace: {}".format(pod_name, pod_namespace))
    container_ids = get_containers(pod_name, pod_namespace)
    print("Current container ids on pod {}: {}", pod_name, container_uds)

    delete_commands = [
        "/bin/sh",
        "docker stop {}".format(container_ids[0])
    ]

    num_container_before_deletion = len(get_containers(pod_name, pod_namespace))
    exec_command(pod_name, pod_namespace, delete_commands)
    num_container_after_deletion = len(get_containers(pod_name, pod_namespace))

    print("Before: {} containers. After: {} containers.".format(num_container_before_deletion, num_container_after_deletion))
    
    # Check if the container reboots
    max_attempts = 10
    cur_attempts = 0

    container_recovers = False

    while cur_attempts < max_attempts and (not container_recovers):
        print("See if container reboots")
        print("Sleeping for 10 seconds...")
        sleep(10)

        num_container_current = len(get_containers(pod_name, pod_namespace))

        if num_container_current > num_container_after_deletion:
            container_recovers = True

        cur_attempts += 1

    if container_recovers:
        print("Container recover successfully")
    else:
        print("Container fails to recover")

if __name__ == "__main__":
    # List of pods in a python list
    pods = get_pods_list()

    # Deleting a pod:
    for name, a in pods.iteritems():
        pod_name = name
        pod_namespace = a[0].namespace
        test_delete_container(pod_name, pod_namespace)

