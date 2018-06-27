from DockerInstance import DockerInstance

a = DockerInstance()
a.start()
a.command('whoami')
a.stop()
