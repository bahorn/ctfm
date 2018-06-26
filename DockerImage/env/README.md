# Env

This directory contains the tools to be installed in the container.

## Layout

In the order they are included in the build.

* Base - Really standard stuff. Should rarely need to change.
* Common - Larger tools (Metasploit) that are better to install earlier in the
build.
* Connectivity - Standard tools to talk to services.
* Dev - Things like `pip` and `git`. Basically for getting stuff up and going.
* Tools - Your generic infosec tooling.
