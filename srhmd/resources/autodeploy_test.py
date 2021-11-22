"""
autodeploy_test.py
Script that pushes srhmd to all robots specified in a config file
"""

import os
import json
import paramiko
import time

def deploy(key, machine, username, password):
    """
    deploy
    Arguments:
        key: String
            ssh public key
        machine: String
            ip address of robot
        username: String
            username of robot host, default just "pi" for raspberry pis
        password: String
            password of robot host, default just "raspberry" for raspberry pis
    Returns:
        None
    """

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(machine['ip'], username=username, password=password)

    print("Deploying on {} ...".format(machine['ip']))

    # Push ssh public key to robots
    client.exec_command('mkdir -p ~/.ssh/')
    client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
    client.exec_command('chmod 644 ~/.ssh/authorized_keys')
    client.exec_command('chmod 700 ~/.ssh/')

    print("\tCreating config: {}".format(machine))

    # Make config in local and push
    with open('config.json', 'w') as outfile:
        json.dump(machine, outfile)
    client.exec_command('mkdir srhmd_conf')
    sftp = client.open_sftp()
    sftp.put('config.json', 'srhmd_conf/config.json')
    sftp.close()

    # Remove config from local
    os.remove("config.json")

    print("\tStarting srhmd ...")
    # Shut down existing srhmd instances
    # docker rm $(docker stop $(docker ps -a -q --filter ancestor=alexcwu1121/srhmd:latest --format="{{.ID}}"))
    _, stdout, _ = client.exec_command('docker rm $(docker stop $(docker ps -a -q ' +
                        '--filter ancestor=alexcwu1121/srhmd:latest ' +
                        '--format="{{.ID}}"))')
    if stdout.channel.recv_exit_status() == 0:
        print("\tSUCCESS: Previous SRHMD instances cleared")
    else:
        print("\tFAIL: Previous SRHMD instances not cleared or none exist")

    # Pull srhmd docker image
    _, stdout, _ = client.exec_command('docker pull alexcwu1121/srhmd:latest')
    if stdout.channel.recv_exit_status() == 0:
        print("\tSUCCESS: SRHMD docker image pulled")
    else:
        print("\tFAIL: SRHMD docker image not pulled")
    time.sleep(5)

    # Run srhmd docker image
    _, stdout, _ = client.exec_command('docker run --network host' +
                                       ' -v /home/pi/srhmd_conf:/srhmd/srhmd_conf alexcwu1121/srhmd:latest')

    print("\n")

if __name__  == "__main__":
    # grab ssh public key
    key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()

    # Assuming default raspberry pi login
    # TODO: figure out a generalizable way to get past password ssh, ...
    #   or just get users to do ssh key pushing in the first place
    username = "pi"
    password = "raspberry"

    # Deploy for each host specified in master config
    with open('config_testing.json') as f:
        data = json.load(f)
    list_of_machines = data["mlist"]
    for machine in list_of_machines:
        try:
            deploy(key, machine, username, password)
        except:
            print("Host unresponsive. Moving on.")

