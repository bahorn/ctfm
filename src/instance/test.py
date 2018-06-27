from DockerInstance import DockerInstance
config = {
    'user':'root',
    'name': 'test',
    'image':'ctfm',
    'test':2,
    'devices':[],
    'volumes':[],
    'ports':[],
    'environment':{},
    'features':[],
    'prefix':'ctfm',
    'memory':'512mb',
    'privileged':False
}
a = DockerInstance(config)
a.start()
a.command('whoami')
a.stop()
