# UPS Monitoring

This directory contains scripts to setup an OPC UA server
to monitor the status of the Uninterrumptible Power Supply (UPS)
unit connected to module two. 

## Linux dependencies

snmp (Used to query the UPS)

## Python dependencies

* Python3
* asyncua
* asyncio

All these dependencies can be installed via pip. We recommend
to create a virtual environment to install these packages.

## Monitoring

NOTE: This assumes that you are working on the RasPi used for 
the UPS monitoring. 

## Setup paths
From the directory where this README is located do

```bash
source setup.sh
```

Note that on the RasPi the global mibs directory
is located in

```bash
$HOME/mibs
```

## Initialize server

To start the OPC-UA server do 

```bash
python ${TOP_DIR}/Source/UPS_with_opcua.py
```

We recommend using nohup to keep the process running
on the background

```bash
nohup python ${TOP_DIR}/Source/UPS_with_opcua.py > ups_server.log 2>&1 &
```

## Check if the server is working

If you want to check that the data is being sent
to the OPC-UA server, you can run 

```bash
python ${TOP_DIR}/Source/retrieve_server_data.py
```

If the data shows up successfuly, it should also be visible 
to the PostgreSQL DB. You can check this by looking at Grafana
and Ignition. 


## Start server after RasPi reboot

The following script is used to start the OPC-UA server after a reboot

```bash
start_server_on_raspi.sh
```

Instructions on how to configure the RasPi to do so can be found [here](https://medium.com/@girishbhasinofficial/configuring-a-script-to-run-at-startup-on-ubuntu-22-04-ffe1f3e649d1)

