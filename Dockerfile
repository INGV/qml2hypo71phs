FROM ubuntu:18.04
LABEL maintainer="Raffaele Di Stefano <raffaele.distefano@ingv.it>"
ENV DEBIAN_FRONTEND=noninteractive 
# Installing all needed applications
RUN apt-get update
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y gcc
RUN apt-get install -y build-essential
RUN apt-get install -y systemd
RUN apt-get install -y wget
# Adding python3 libraries
RUN python3 -m pip install numpy
RUN python3 -m pip install obspy
COPY qml2hypo71.py /opt
COPY ws_agency_route.conf /opt
