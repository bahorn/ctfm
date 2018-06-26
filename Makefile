TAGNAME=ctfm

build:
	docker build -t $(TAGNAME) ./DockerImage
