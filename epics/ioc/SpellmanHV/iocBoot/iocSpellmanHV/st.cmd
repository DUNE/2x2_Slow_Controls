#!../../bin/linux-x86_64/SpellmanHV

#- You may have to change SpellmanHV to something else
#- everywhere it appears in this file

##setup environment

< envPaths
epicsEnvSet("STREAM_PROTOCOL_PATH","../../db")

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/SpellmanHV.dbd"
SpellmanHV_registerRecordDeviceDriver pdbbase

## setup ASYN port for Ethernet connection
drvAsynIPPortConfigure("SpellmanHV", "192.168.197.84:50001", 0,0,0)

## Debugging
#asynSetTraceIOMask("SpellmanHV",-1,0xff) # check what 0x4 is doing
#asynSetTraceIOMask("SpellmanHV",0,HEX|ESCAPE)
#asynSetTraceMask("SpellmanHV",-1,0xff)
#asynSetTraceIOTruncateSize("SpellmanHV",-1, 1024)

## Load record instances
dbLoadRecords("db/devSpellmanHVRead.db", "PORT=SpellmanHV,BUS=0")

cd "${TOP}/iocBoot/${IOC}"
iocInit
#####
##### Set Initial Variables
< "${TOP}/iocBoot/${IOC}/init.cmd"
