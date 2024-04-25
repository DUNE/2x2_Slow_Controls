TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#USR_CFLAGS += -I/usr/local/include        #Path to snmp if ness.
USR_CFLAGS += `net-snmp-config --cflags`
USR_CFLAGS += -DNETSNMP_NO_INLINE

USR_LDFLAGS += `net-snmp-config --libs`
PROD_LDLIBS += `net-snmp-config --libs`

USR_CFLAGS += $(shell $(PERL) ../getNetSNMPversion.pl)
USR_CPPFLAGS += $(shell $(PERL) ../getNetSNMPversion.pl)

#==================================================
# Build an IOC support library
LIBRARY_IOC += devSnmp

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxxRecord
# install devXxxSoft.dbd into <top>/dbd
DBD += devSnmp.dbd

# The following are compiled and added to the Support library

devSnmp_SRCS += snmpRegister.cpp
devSnmp_SRCS += snmpSessShow.c
devSnmp_SRCS += devSnmp.cpp

devSnmp_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================
# build an ioc application

PROD_IOC = MPOD
# snmp.dbd will be created and installed
DBD += MPOD.dbd

# snmp.dbd will be made up from these files:
MPOD_DBD += base.dbd
MPOD_DBD += devSnmp.dbd

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
MPOD_SRCS += MPOD_registerRecordDeviceDriver.cpp
MPOD_SRCS_DEFAULT += MPODMain.cpp
MPOD_SRCS_vxWorks += -nil-

# The following adds support from base/src/vxWorks
MPOD_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

MPOD_LIBS += devSnmp

# NOTE: To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file

ifneq ($(SNCSEQ),)
    # This builds sncExample as a component of snmp
    MPOD_SNCFLAGS += +r
    MPOD_DBD += sncExample.dbd
    MPOD_SRCS += sncExample.stt
    MPOD_LIBS += seq pv

    # The following builds sncProgram as a standalone application
    PROD_HOST += sncProgram
    sncProgram_SNCFLAGS += +m
    sncProgram_SRCS += sncProgram.st
    sncProgram_LIBS += seq pv
    sncProgram_LIBS += $(EPICS_BASE_HOST_LIBS)
endif

MPOD_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

