from DockerInstance import DockerInstance

a = DockerInstance({'features':['X']})
a.start()
a.command('bash')
a.stop()
