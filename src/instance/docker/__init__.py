import docker

from instance import Instance
import utils as DockerUtils

class DockerInstance(Instance):
    def __init__(self, config):
        super().__init__(self, config)
        self.client = docker.from_env()
        # Parse the configuration provided into a from that can be used by the
        # docker library.
        dockerDevices = DockerUtils.devices(self.config.devices)
        dockerVolumes = DockerUtils.volumes(self.config.volumes)
        dockerPorts = DockerUtils.ports(self.config.ports)
        dockerEnvironment = DockerUtils.environment(
            self.config.environment)
        # Create the Container instance
        self.container = self.client.containers.create(
            image=self.config.image,
            name=InstanceUtils.formatName(self.config.name),
            ports=self.config.ports,
            mem_limit=self.config.memory,
            devices=dockerDevices,
            volumes=dockerVolumes,
            ports=dockerPorts,
            environment=dockerEnvironment,
            privileged=self.config.privileged
            detach=True
        )

    def start(self):
        self.container.start()

    def stop(self):
        self.container.stop()

    def command(self, command=None):
        if command == None:
            command = self.config.shellCommand
        self.container.shell(command)
