# UPS 

This directory containts scrips to setup an OPCUA server
to monitor the status of the Uninterrumpted Power Supply (UPS)
unit connected to module two. 

## Linux dependencies

snmp (Used to query the UPS)

## Python dependencies

* Python3
* asyncua
* asyncio
* influxdb (for possible Grafana integration)

All these dependencies can be installed via pip. We recommend
to create a virtual environment to install these packages.

## Setup paths
```bash
source setup.sh
```

## Initialize server
```bash
python ${TOP_DIR}/Source/UPS_with_opcua.py
```

## Monitroing
```bash
python ${TOP_DIR}/Source/retrieve_server_data.py
```
For now, this script only prints the actual value 
of a set of UPS features to the terminal. 


