# gsw-ait
AIT groundstation for nos3

## Introduction

This software implements a telemetry de-commutation and command encoding server for NASA’s nos3/STF-1 simulation engine.  It leverages a JPL framework called AIT to provide core functionality.  In fact, the majority of this repo is OOB or slightly modified AIT modules which provide the core networking, de-commutation, encoding and storage capabilities.  Work in this repository was primarily focused on developing the corresponding configuration files necessary for integration with nos3.  These files include the telemetry and command definitions as well as the primary configuration file that defines network endpoints.

## Dependencies
    - Docker
    - Docker Compose
    - Make

## Quick Start

A basic demonstration of AIT’s capabilities can be seen by running make on the supplied Makefile.  This will create four services:

    - gsw-ait: The core de-commutation and encoding software
    - nos-fsw: A basic endpoint to receive commands
    - telem: replays a nos3 telemetry recording on repeat for ingestion by gsw-ait
    - Influxdb: a database to store the de-commutated telemetry

To run the demo, simply clone the repository and then run

```
make run
```

from the top level of the repository.  You can then use your preferred graphical or command line utility to view the data in InfluxDB or you can connect a UI (insert link here) to the defined websocket port.

## Default Endpoints and Ports

The following are the default ports for communication with various endpoints and services assuming you have started the services with the supplied docker compose file:

    - influxdb   : influxdb:8086
    - command rx : gsw-ait:3075
    - command tx : nos_fsw:5012
    - telem rx   : 0.0.0.0:5013
    - websocket  : localhost:8001

## Current Limitations

AIT does nor currently support some command data types (such as strings or bytearrays) and consequently some nos3 commands cannot be implemented yet using AIT.  At the time of writing, approx 95% of telemetry and command packets are implemented.

Additionally, the API needs to be extended to provide full functionality.  Currently many endpoints are stubbed, faked or not implemented. Further work needs to be done on creating cookies and secure session.  Core realtime telemetry and commanding ARE implemented.
