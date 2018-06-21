FROM kalilinux/kali-linux-docker:latest

## Upgrade the packages.

RUN apt-get -y update
RUN apt-get -y upgrade

## Install the packages in stages to avoid having to rebuild everything 
## due to changes in the later stages.

# 1. Base Environment

COPY env/base.lst /tmp/base.lst
RUN xargs apt-get -y install < /tmp/base.lst

# 2. Common
# Good place for larger tools.
COPY env/common.lst /tmp/common.lst
RUN xargs apt-get -y install < /tmp/common.lst

# 3. Connectivity
# Got to talk to stuff :)

COPY env/connectivity.lst /tmp/connectivity.lst
RUN xargs apt-get -y install < /tmp/connectivity.lst

# 4. Dev tools
# Some tools like python need things like pip, etc.

COPY env/dev.lst /tmp/dev.lst
RUN xargs apt-get -y install < /tmp/dev.lst

# 5. Infosec Tools
# Usual stuff.

COPY env/tools.lst /tmp/tools.lst
RUN xargs apt-get -y install < /tmp/tools.lst

## Cleanup

RUN ["rm","/tmp/*.lst"]

## Add a user.

RUN adduser --disabled-password --gecos "" --shell /bin/bash user
RUN echo "user ALL=(ROOT) NOPASSWD:ALL" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user

## Default script.

COPY ./bootstrap.sh /bootstrap.sh
RUN ["chmod","+x","/bootstrap.sh"]
CMD /bootstrap.sh
