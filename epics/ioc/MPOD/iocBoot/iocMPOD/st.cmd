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
epicsEnvSet("ACD-MPOD2","HOST=acd-mpod2,crate=2")

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
dbLoadTemplate("db/VGA_Mod0.sub","${ACD-MPOD1},${WIENER_SNMP}")
dbLoadTemplate("db/VGA_Mod1.sub","${ACD-MPOD1},${WIENER_SNMP}")
dbLoadTemplate("db/VGA_Mod2.sub","${ACD-MPOD2},${WIENER_SNMP}")
dbLoadTemplate("db/VGA_Mod3.sub","${ACD-MPOD2},${WIENER_SNMP}")

## RTDs
#dbLoadTemplate("db/RTD_Mod0.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/RTD_Mod1.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/RTD_Mod2.sub","${ACD-MPOD2},${WIENER_SNMP}")
#dbLoadTemplate("db/RTD_Mod3.sub","${ACD-MPOD2},${WIENER_SNMP}")

## PACMAN
#dbLoadTemplate("db/PAC_Mod0.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/PAC_Mod1.sub","${ACD-MPOD1},${WIENER_SNMP}")
#dbLoadTemplate("db/PAC_Mod2.sub","${ACD-MPOD2},${WIENER_SNMP}")
#dbLoadTemplate("db/PAC_Mod3.sub","${ACD-MPOD2},${WIENER_SNMP}")

#cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=dunecet"
