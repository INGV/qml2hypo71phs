# qml2hypo71phs

The qml2hypo71phs.py code is included into the present docker.

The docker is used to parse a full QuakeML (xml) file containing information on hypocenter and related arrival times picks, and convert all to hypo71 phase input file.

Beyond column 78 (^) of the output file, additional information are included on each phase line about station, network and event.

The following line is taken from the example output:
 
VOBA P 0Z210203152652.99       55.00 S 1      40.85                           HNZIV--    EVID:26031941,ORID:86811231,V:100
                                                                             ^
channel: 79-81
network: 82-83
location: 84-85
eventid,originid,originversion: 90-> free format comma separated list. These information allow to interact back with the QuakeML file.

The source code has a specific usage to which the docker has its simplified interface, so the usere does not need to know it.

Anyway, only for information completeness here it is:

```
usage: qml2hypo71phs.py [-h] [--qmlin QMLIN] [--eventid EVENTID] [--version VERSION] [--conf CONF] [--agency AGENCY]

optional arguments:
  -h, --help         show this help message and exit
  --qmlin QMLIN      Full path to qml event file
  --eventid EVENTID  INGV event id
  --version VERSION  Agency coding origin version type (default: preferred) preferred,all, or an integer for known version
                     numbers
  --conf CONF        needed with --eventid agency webservices routes list type (default: ./ws_agency_route.conf)
  --agency AGENCY    needed with --eventid agency to query for (see routes list in .conf file) type (default: ingv)
```

## Quickstart
### Build docker
```
$ git clone git@github.com:INGV/qml2hypo71phs.git
$ cd qml2hypo71phs
$ docker build --tag qml2hypo71phs . 
```

### Run docker
to show syntax:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input qml2hypo71phs 
```

example:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input qml2hypo71phs --qmlin /opt/input/quakeml.xml
```

#### Docker CLI
To override the `ENTRYPOINT` directive and enter into the Docker container, run:
```
$ docker run --rm -it --user $(id -u):$(id -g) --entrypoint=bash qml2hypo71phs
```

# Contribute
Please, feel free to contribute.

# Author
(c) 2021 Raffaele Distefano raffaele.distefano[at]ingv.it

(c) 2021 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
