#!../../bin/linux-x86_64/testioc

#- You may have to change pdu to something else
#- everywhere it appears in this file

< envPaths
epicsEnvSet("STREAM_PROTOCOL_PATH","../../db")

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/testioc.dbd"
testioc_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadRecords("db/devtestioc.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=sbnddcs"
