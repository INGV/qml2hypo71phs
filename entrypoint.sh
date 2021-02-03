#!/bin/bash
#
#
# (c) 2021 Valentino Lauciani <valentino.lauciani@ingv.it>,
#          Raffaele Distefano <raffaele.distefano@ingv.it>,
#          Istituto Nazione di Geofisica e Vulcanologia.
# 
#####################################################

# Check input parameter
if [[ -z ${@} ]]; then
        echo ""
	/usr/bin/python3 /opt/qml2hypo71.py -h
        echo ""
        exit 1
fi

# run command
/usr/bin/python3 /opt/qml2hypo71.py $@
