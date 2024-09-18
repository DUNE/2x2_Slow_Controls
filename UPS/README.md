# UPS Monitoring

This directory containts scripts to setup an OPC UA server
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


From the directory where this README is located do
## Setup paths
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

Nevertheless, we recommend using nohup to keep the process running
on the background

```bash
nohup python Source/UPS_with_opcua.py > ups_server.log 2>&1 &
```

## Check if the server is working

If you want to check that the data is correctly being send
to the OPC-UA server, you can run 

```bash
python ${TOP_DIR}/Source/retrieve_server_data.py
```

If the data shows up successfuly, it will also be visible 
to the PostgreSQL DB. Then, you should check if data is being
correctly displayed in Grafana and Ignition. 


