#!../../bin/linux-x86_64/MPOD

#- You may have to change wiener to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/MPOD.dbd"
MPOD_registerRecordDeviceDriver pdbbase

## Load record instances MPOD records
devSnmpSetParam("DebugLevel",1)
devSnmpSetParam("SessionTimeout", "100000000")
epicsEnvSet("WIENER_SNMP","COMMUNITY=guru,W=WIENER-CRATE-MIB")
epicsEnvSet("ACD-MPOD1","HOST=acd-mpod1,crate=1")
epicsEnvSet("ACD-MPOD1","HOST=acd-mpod2,crate=2")

## Crate
#dbLoadRecords("db/crate.db","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadRecords("db/crate.db","${ACD-MPOD2},${WIENER_SNMP}")

## Slots
#dbLoadRecords("db/slot_slot0.db","${ACD-MPOD1},${WIENER_SNMP},slot=0")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD1},${WIENER_SNMP},slot=1")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD1},${WIENER_SNMP},slot=2")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD1},${WIENER_SNMP},slot=3")

#dbLoadRecords("db/slot_slot0.db","${ACD-MPOD2},${WIENER_SNMP},slot=0")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD2},${WIENER_SNMP},slot=1")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD2},${WIENER_SNMP},slot=2")
#dbLoadRecords("db/slot_slot1-3.db","${ACD-MPOD2},${WIENER_SNMP},slot=3")

## VGAs
dbLoadTemplate("db/Mod0_VGA.sub","${ACD-MPOD1},${WIENER_SNMP}")
dbLoadTemplate("db/Mod1_VGA.sub","${ACD-MPOD1},${WIENER_SNMP}")
dbLoadTemplate("db/Mod3_VGA.sub","${ACD-MPOD2},${WIENER_SNMP}")
dbLoadTemplate("db/Mod4_VGA.sub","${ACD-MPOD2},${WIENER_SNMP}")

## RTDs
#dbLoadTemplate("db/Mod0_RTD.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod1_RTD.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod2_RTD.sub","${ACD-MPOD2},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod3_RTD.sub","${ACD-MPOD2},${WIENER_SNMP}")

## PACMAN
#dbLoadTemplate("db/Mod0_PACMAN.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod1_PACMAN.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod2_PACMAN.sub","${ACD-MPOD2},${WIENER_SNMP}")
#dbLoadTemplate("db/Mod3_PACMAN.sub","${ACD-MPOD2},${WIENER_SNMP}")

#cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=dunecet"
