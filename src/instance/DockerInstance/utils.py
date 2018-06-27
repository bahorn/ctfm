# Utilities to convert our description of a service into one suitable for
# docker.

def devices(devices):
    dockerDevices = []
    # We assume rwm as the default permission
    for device in devices:
        if 'device' not in features:
            raise ValueError('Expected a Device')
        if 'mount' not in features:
            features['mount'] = features['device']
        if 'mode' not in features:
            features['mode'] = 'rwm'
        dockerDevices.append("{}:{}:{}".format(
            features['device'], features['mount'], features['mode']))
    return dockerDevices

# Nothing really needs to be done as we'd get it as a Dict anyway.
def environment(environment):
    return environment

def ports(ports):
    dockerPorts = {}
    return dockerPorts

def volumes(volumes):
    dockerVolumes = {}
    for volume in volumes:
        pass
    return dockerVolumes

