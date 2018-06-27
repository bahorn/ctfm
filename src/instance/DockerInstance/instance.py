import docker
import os

from instance import Instance
import instanceUtils as InstanceUtils
import DockerInstance.utils as DockerUtils
import DockerInstance.features as DockerFeatures


class DockerInstance(Instance):
    features = {
        "X":DockerFeatures.enableX
    }
    # We ignore the features passed to this class.
    def __init__(self, config={}, features=None):
        super().__init__(config, self.features)
        self.client = docker.from_env()
        self.formatedName = InstanceUtils.formatName(self.config['name'],
                                                     self.config['prefix'])
        # Parse the configuration provided into a from that can be used by the
        # docker library.
        self.dockerDevices = DockerUtils.devices(self.config['devices'])
        self.dockerVolumes = DockerUtils.volumes(self.config['volumes'])
        self.dockerPorts = DockerUtils.ports(self.config['ports'])
        self.dockerEnvironment = DockerUtils.environment(
            self.config['environment'])
        # Enable the features asked for.
        self._enableFeatures()
        # Create the Container instance
        self.container = self.client.containers.create(
            image=self.config['image'],
            name=self.formatedName,
            mem_limit=self.config['memory'],
            devices=self.dockerDevices,
            volumes=self.dockerVolumes,
            ports=self.dockerPorts,
            environment=self.dockerEnvironment,
            privileged=self.config['privileged'],
            detach=True
        )

    def start(self):
        self.container.start()

    def stop(self):
        self.container.kill()
        self.remove()

    def remove(self):
        self.container.remove()

    def command(self, command=None):
        user = self.config['user']
        if command == None:
            command = self.config['shellCommand']
        self._runCommand(command, user)

    def _runCommand(self, command, user):
        # I couldn't get exec_run to work correctly so I settled on this...
        os.system('docker exec -it -u {} {} {}'.format(
            user, self.formatedName, command))

    def _enableFeatures(self):
        # cycle through the features that the user requests and run the script
        # to activate them.
        for feature in self.config['features']:
            self.features[feature](self)

