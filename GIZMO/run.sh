#!/bin/bash
#
# Script: run.sh
# Description: Start the TTI podman container after ensuring previous container stopped
# Author: Renzo Vizarreta
# Date: May 22nd, 2024

###############################################################
# Make sure all containers are stopped
podman-compose -f compose.yaml down

###############################################################
# Find local ip address for ssh connection with influxdb
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
podman-compose -f compose.yaml build --no-cache && podman-compose -f compose.yaml up 