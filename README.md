# qml2hypo71phs

Docker used to . . .

## Quickstart
### Build docker
```
$ git clone git@github.com:INGV/qml2hypo71phs.git
$ cd qml2hypo71phs
$ docker build --tag qml2hypo71phs . 
```

### Run docker
Run:
```
$ docker run --rm -v $(pwd)/input:/opt/inout qml2hypo71phs <file>.quakeml 
```

#### Docker CLI
To override the `ENTRYPOINT` directive and enter into the Docker container, run:
```
$ docker run --rm -it --entrypoint=bash qml2hypo71phs
```

# Contribute
Please, feel free to contribute.

# Author
(c) 2021 Raffaele Distefano raffaele.distefano[at]ingv.it

(c) 2021 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
