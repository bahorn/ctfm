# CTFm

A easy to modify Docker Image and a tool to manage instances of it.

Written to make doing CTFs less of a pain.

## Details

The image is based on the Kali base images, with whatever I ended up needing to
do stuff on HackTheBox.

## Usage

Build the Docker image with `make`, then use the `ctfm` script to spawn up
instances.

All the flags are optional.

All the options:
```
ctfm start <name> --ports 4444:tcp 3333:udp 5555-5560:both 2222 \
    --volumes `pwd`/test:/mnt/test:writable `pwd`/test2:/mnt/test2 --enableX
     --privileged --memory=1024mb --image ctfm:latest
```

Get a shell in the container:
```
ctfm shell <name> --user user --command whoami
```

Stop the container:
```
ctfm stop <name>
```

List all containers created by this tool:
```
ctfm ls
```
