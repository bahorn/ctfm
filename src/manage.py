#!/usr/bin/env python3

import docker
import os

import utils as CtfmUtils
import defaults as CtfmDefaults

# Main class for this script.
class CtfmManage:
    def __init__(self, prefix=CtfmDefaults.prefix):
        self.client = docker.from_env()
        # So we can find all our images
        self.prefix = prefix

    def start(self, name, ports=CtfmDefaults.ports, memory=CtfmDefaults.memory,
              volumes=CtfmDefaults.volumes, enableX=CtfmDefaults.enableX,
              privileged=CtfmDefaults.privileged, image=CtfmDefaults.image,
              command=CtfmDefaults.startCommand):
        dockerDevices = []
        dockerEnvironment = {}
        dockerPorts = {}
        dockerVolumes = {}
        # Get the volumes and ports into a usable form.
        self._scanVolumes(volumes, dockerVolumes)
        self._scanPorts(ports, dockerPorts)

        # Setup the X server so we can run GUI programs in the container.
        if enableX == True:
            self._xEnable(dockerDevices, dockerEnvironment, dockerVolumes)
        # Build our Container.
        return self.client.containers.run(
            image=image,
            name=self._formatName(name),
            ports=dockerPorts,
            mem_limit=memory,
            detach=True,
            remove=True,
            devices=dockerDevices,
            volumes=dockerVolumes,
            environment=dockerEnvironment,
            command=command,
            privileged=privileged
        )

    # Kill it.
    def stop(self, name):
        return self.client.containers.get(self._formatName(name)).kill()

    # Get our shell
    def shell(self, name, command=CtfmDefaults.shellCommand,
              user=CtfmDefaults.user):
        # I couldn't get exec_run to work correctly so I settled on this...
        os.system('docker exec -it -u {} {} {}'.format(
            user, self._formatName(name), command))

    def ls(self):
        containers = []
        for container in self.client.containers.list():
            if self.prefix+'-' in container.name[0:len(self.prefix)+1]:
                containers.append(container)
        return containers

    def _formatName(self, name):
        return "{}-{}".format(self.prefix, name)

    # Get X Going in the container.
    def _xEnable(self, dockerDevices, dockerEnvironment, dockerVolumes,
                 display=CtfmDefaults.display, xsock=CtfmDefaults.xsock):
        # Audio Device
        dockerDevices.append("/dev/snd:/dev/snd:rwm")
        # X auth.
        xauth = '/tmp/.docker.xauth'
        # HACK
        os.system(
            'xauth nlist :0 | sed -e "s/^..../ffff/" | xauth -f {} nmerge -'
            .format(xauth)
        )
        # Set the environment.
        dockerEnvironment['XAUTHORITY'] = xauth
        dockerEnvironment['DISPLAY'] = display
        # Files we need to expose.
        dockerVolumes[xauth] = CtfmUtils.volumes(xauth, writable=True)
        dockerVolumes[xsock] = CtfmUtils.volumes(xsock, writable=True)

    def _scanVolumes(self, volumes, dockerVolumes):
        for volume in volumes:
            details = volume.split(':')
            writable = False
            if len(details) == 3:
                if details[2] == 'writable':
                    writable = True
                elif details[2] == 'readonly':
                    writable = False
                else:
                    raise ValueError(
                        "Volume %s not in correct format".format(volume))

            dockerVolumes[details[0]] = \
                CtfmUtils.volumes(details[1], writable=writable)

    # stupid lazy hacks.
    def _scanPorts(self, ports, dockerPorts):
        for port in ports:
            details = port.split(':')
            if len(details) == 1:
                proto = 'tcp'
            elif len(details) == 2:
                proto = details[1]
            tcp = False
            udp = False
            if proto in ['tcp', 'both']: tcp = True
            if proto in ['udp', 'both']: udp = True
            newPorts = CtfmUtils.ports(int(details[0]), int(details[0]),
                                        tcp=tcp, udp=udp)
            for key in newPorts.keys():
                dockerPorts[key] = newPorts[key]
