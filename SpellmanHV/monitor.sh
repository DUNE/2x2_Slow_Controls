#!/bin/bash
#
# Script: run.sh
# Description: Start the podman containers after ensuring all containers are stopped
# Author: Renzo Vizarreta
# Date: March 27th, 2024

###############################################################
# Make sure all containers are stopped
podman-compose -f compose.yaml down

###############################################################
# Start podman container
podman-compose -f compose.yaml up -d