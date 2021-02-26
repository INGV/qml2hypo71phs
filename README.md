[![License](https://img.shields.io/github/license/INGV/qml2hypo71phs.svg)](https://github.com/INGV/qml2hypo71phs/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/INGV/qml2hypo71phs.svg)](https://github.com/INGV/qml2hypo71phs/issues)

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/ingv/qml2hypo71phs)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/ingv/qml2hypo71phs?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/ingv/qml2hypo71phs)

# qml2hypo71phs [![Version](https://img.shields.io/badge/dynamic/yaml?label=ver&query=softwareVersion&url=https://raw.githubusercontent.com/INGV/qml2hypo71phs/master/publiccode.yml)](https://github.com/INGV/qml2hypo71phs/blob/master/publiccode.yml) [![CircleCI](https://circleci.com/gh/INGV/qml2hypo71phs/tree/master.svg?style=svg)](https://circleci.com/gh/INGV/qml2hypo71phs/tree/master)

Docker used to . . .

## Quickstart
### Docker image
To obtain *qml2hypo71phs* docker image, you have two options:

#### 1) Get built image from DockerHub (*preferred*)
Get the last built image from DockerHub repository:
```
$ docker pull /ingv/qml2hypo71phs
```

#### 2) Build by yourself
First, clone the git repository
```
$ git clone https://github.com/INGV/qml2hypo71phs.git
$ cd qml2hypo71phs
$ docker build --tag ingv/qml2hypo71phs . 
```

in case of errors, try:
```
$ docker build --no-cache --pull --tag ingv/qml2hypo71phs . 
```

### Run docker
To run the container, use the command below; the `-v` option is used to "mount" working directory into container:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input ingv/qml2hypo71phs 
```

example:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input ingv/qml2hypo71phs --qmlin /opt/input/quakeml.xml
```

#### Docker CLI
To override the `ENTRYPOINT` directive and enter into the Docker container, run:
```
$ docker run --rm -it --user $(id -u):$(id -g) --entrypoint=bash qml2hypo71phs
```

## Update Docker image from DockerHub
Get last Docker image from DockerHub repository:
```
$ docker pull ingv/qml2hypo71phs
```

# Contribute
Please, feel free to contribute.

# Author
(c) 2021 Raffaele Distefano raffaele.distefano[at]ingv.it

(c) 2021 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
