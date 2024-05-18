#!/bin/bash
#
# Script: run.sh
# Description: Start the podman container for MINERvA log reader after ensuring old containers are stopped
# Author: Renzo Vizarreta
# Date: May 16th, 2024

###############################################################
# Make sure all containers are stopped
podman-compose -f compose.yaml down

###############################################################
# Start podman container
podman-compose -f compose.yaml build --no-cache && podman-compose -f compose.yaml up -d