#!/bin/bash
#
# Script: run.sh
# Description: Start the podman containers after ensuring all containers are stopped
# Author: Renzo Vizarreta
# Date: February 17th, 2024

###############################################################
# Make sure all containers are stopped
podman-compose -f compose.prod.yaml down

###############################################################
# Find local ip address for ssh connection with gizmo
# We do this because ip address may change 
IFS=' ' read -ra IP_ADDRESSES <<< "$(hostname -I)"

for ip in "${IP_ADDRESSES[@]}"; do
    if [[ $ip == 192* ]]; then
        export LOCAL_IP="$ip"
        echo "Found IP address starting with 192: $LOCAL_IP"
        break  
    fi
done

###############################################################
# Start podman container
podman-compose -f compose.prod.yaml up --build -d