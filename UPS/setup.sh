#!/usr/bin/bash
echo "Setting up paths..."
TOP_DIR=$PWD
UPS_MIB_DIR=${TOP_DIR}/mibs_ups
GLOBAL_MIB_DIR=/usr/share/snmp/mibs
export TOP_DIR
export UPS_MIB_DIR
export GLOBAL_MIB_DIR
echo "TOP_DIR: ${TOP_DIR}"
echo "UPS_MIB_DIR: ${UPS_MIB_DIR}"
echo "GLOBAL_MIB_DIR: ${GLOBAL_MIB_DIR}"
