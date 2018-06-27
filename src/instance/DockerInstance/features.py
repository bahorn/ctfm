#!/usr/bin/env python3

import os

## These all directly modify the instance after the user passed device,
## volumes, ports, etc. So they need to add 

# Allows the container to use the hosts X server.
def enableX(instance):
    display = instance.config['display']
    xsock = instance.config['xsock']
    xauth = instance.config['xauth']
    # Added the devices needed.
    instance.dockerDevices.append('/dev/snd:/dev/snd:rwm')
    # Authorize us
    os.system(
        'xauth nlist {} | sed -e "s/^..../ffff/" | xauth -f {} nmerge -'
        .format(display, xauth)
    )
    # Set the environment variables
    instance.dockerEnvironment['XAUTHORITY'] = xauth
    instance.dockerEnvironment['DISPLAY'] = display
    # Mount the files needed.
    instance.dockerVolumes[xauth] = {'bind': xauth, 'mode': 'rw'}
    instance.dockerVolumes[xsock] = {'bind': xsock, 'mode': 'rw'}
