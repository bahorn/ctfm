#!/usr/bin/env python3

# Handles how volumes are read from the command line.
def volumes(path, writable=True):
    mode = 'rw'
    if writable == False: mode = 'ro'
    return {'bind': path, 'mode':mode}

# Converts the port description into the form required by docker-py
def ports(containerPort, hostPort, hostInterface='0.0.0.0', udp=False,
          tcp=True):
    ports = {}
    if tcp==True:
        ports['{}/tcp'.format(containerPort)] = (hostInterface, hostPort)
    if udp==True:
        ports['{}/udp'.format(containerPort)] = (hostInterface, hostPort)

    return ports
