#!/usr/bin/env python3

import binascii
import os
import defaults

class FeatureError(Exception):
    pass

def uniqueName():
    # sorry, I'm 32,000 above Mogadishu and forgot the method to get `bytes` to
    # be a nice string, so I did this.
    return binascii.hexlify(os.urandom(8)).__str__()[2:-1]

# Verifies a configuration, setting values that aren't currently set.
# * This should be cleaned up. * 
def validateConfig(config, features):
    # The following are required to be in the config:
    # user, name, image, devices, volumes, ports, environment, features,
    # prefix, memory and privileged
    # So we'll set the default values here if they aren't already set.

    # Name of the Container
    if 'name' not in config:
        # generate a random name.
        config['name'] = uniqueName()
    # Prefix to the name so we can identify the containers easily.
    if 'prefix' not in config:
        config['prefix'] = defaults.prefix
    # User in the container to run the commands as
    if 'user' not in config:
        config['user'] = defaults.user
    # Docker image to use.
    if 'image' not in config:
        config['image'] = defaults.image
    # Features like X, GPU access, etc.
    if 'features' not in config:
        config['features'] = defaults.features
    # Hardware for the container.
    if 'devices' not in config:
        config['devices'] = defaults.devices
    if 'volumes' not in config:
        config['volumes'] = defaults.volumes
    if 'ports' not in config:
        config['ports'] = defaults.ports
    if 'environment' not in config:
        config['environment'] = defaults.environment
    if 'memory' not in config:
        config['memory'] = defaults.memory
    if 'privileged' not in config:
        config['privileged'] = defaults.privileged
    if 'display' not in config:
        config['display'] = defaults.display
    if 'xsock' not in config:
        config['xsock'] = defaults.xsock
    if 'xauth' not in config:
        config['xauth'] = defaults.xauth
    # Now check everything is fine.
    ## Are the features actually supported by the Instance type.
    for feature in config['features']:
        if feature not in features:
            raise FeatureError()
    ## Devices in the correct format
    ## Volumes in the correct format
    ## Ports in the correct format
    ## memory is valid
    ## Types of everything is correct.
    return config

def formatName(name, prefix):
    return "{}-{}".format(prefix, name)
