#!/usr/bin/bash

##########################
#### This script starts the OPC-UA server for you
#### The RasPi runs this scripts everytime the its rebooted 
##########################

# Activate python environment 
source /home/acd-pi-01/WorkDir/ups_env/bin/activate

# Go to UPS dir

cd home/acd-pi-01/WorkDir/2x2_Slow_Controls/UPS

# Setup directories

source setup.sh

# Start the server 
# Store the nohup output into a log file
current_datetime=$(date +"%Y-%m-%d-%H:%M:%S")

nohup python Source/UPS_with_opcua.py > ${TOP_DIR}/ups_server_${current_datetime}.log 2>&1 &
