#!/usr/bin/env python3

# Just the defaults for the image to create.

memory = '512mb'
volumes = []
ports = []
prefix = 'ctfm'
enableX = False
privileged = False
image = 'ctfm:latest'
startCommand =['tail','-f','/dev/null']
shellCommand =['/bin/sh']
user = 'root'
display = ':0'
xsock = '/tmp/.X11-unix'
