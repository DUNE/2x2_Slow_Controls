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

Note: After a restart, it will take a few minutes before the data
shows up in Grafana and Ignition. 


## Start server after RasPi reboot

To restart the server after a RasPi reboot we use a crontab. The command
that is currently configured in the RasPi is described in 

```bash
ups_crontab_cmd.txt
```

If you need to modify the crontab config file, once logged in the RasPi you should do

```bash
crontab -e 
```

To test your modifications after a reboot we suggest to create a log file
in the crontab and then reboot the RasPi from the terminal doing

```bash
sudo reboot 
```

## Kill the server manually

To kill the process associated with the server, first find its process code doing

```bash 
ps -ef | grep UPS_with_opcua.py
```
Then 

```bash 
kill server-code 
```

Where server-code is the PID returned by ps.


## Appendix

### SNMP installation

1.- To install snmp run: 

```bash
sudo apt install snmpd snmp libsnmp-dev
```

2.- Standard mib files do not come with snmp, you need to install them:

```bash
sudo apt-get install snmp-mibs-downloader
sudo download-mibs
```
by default mibs files are installed in the following path:

```bash
/usr/share/snmp/mibs
```

### SNMP commands 

The two commands that we typicaly use for monitoring are snmpwalk and snmpget. 

- snmpwalk: This command navigates the tree of Object Identifiers (OIDs) of a network device and prints the value retrieved for each OID.

- snmpget: This command retrieves the value of just one OID that you have to specify at the moment of executing the command. 

### UPS examples 

```bash
snmpwalk -v 3 -M +./mibs_ups/ -m ALL  -u readonly -c public 192.168.197.92 xupsMIB
```
In this example, we tell snmp to use v3 since it is the version equired to read the UPS mibs. We also tell snmp to look at the mib files contained in the /mibs_ups directory and to include all other visible mibs using -m ALL. The last two arguments are the IP address of the network device (in this example the UPS) and the subset of OIDs you want to query (In this case snmp will print all OIDs associated to xups). If you don't specify a subset OIDs it will just scan all the OIDs.

```bash
snmpget -v 3 -M +./mibs_ups -m all -u readonly -c public 192.168.197.92 xupsBatteryFailure.0
```

In this example the configuration is almost identical to snmpwalk, but this time we are just quering one specific value. This command asks snmp if the batery of the UPS is failing or not. This action will return a boolean value. 

