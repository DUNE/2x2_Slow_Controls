record(ai, "Mod$(module)-$(device)/outputMeasurementCurrent")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputMeasurementCurrent.u$(slot)0$(channel) Float: 100 Fn")
    field(SCAN,".2 second")
    field(EGU,"A")
    field(DESC,"current")
    field(MDEL,"0.1")
    field(ADEL,"0.1")
    field(PREC, "1")
    field(HIHI,"${Ihihi}")
    field(HIGH,"${Ihigh}")
    field(LOW,"${Ilow}")
    field(LOLO,"${Ilolo}")
    field(LLSV, "${Illsv}")
    field(LSV, "${Ilsv}")
    field(HSV, "${Ihsv}")
    field(HHSV, "${Ihhsv}")
}

record(ai, "Mod$(module)-$(device)/outputMeasurementSenseVoltage")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputMeasurementSenseVoltage.u$(slot)0$(channel) Float: 100")
    field(SCAN,".2 second")
    field(EGU,"V")
    field(DESC,"Channel sense voltage read")
    field(MDEL,"0.01")
    field(ADEL,"0.01")
    field(PREC, "3")
    field(HIHI,"${Vhihi}")
    field(HIGH,"${Vhigh}")
    field(LOW,"${Vlow}")
    field(LOLO,"${Vlolo}")
    field(LLSV, "${Vllsv}")
    field(LSV, "${Vlsv}")
    field(HSV, "${Vhsv}")
    field(HHSV, "${Vhhsv}")
}

record(ai, "Mod$(module)-$(device)/outputMeasurementTerminalVoltage")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputMeasurementTerminalVoltage.u$(slot)0$(channel) Float: 100")
    field(SCAN,".2 second")
    field(EGU,"V")
    field(DESC,"Channel terminal voltage read")
    field(MDEL,"0.01")
    field(ADEL,"0.01")
    field(PREC, "3")
}

record(ao, "Mod$(module)-$(device)/outputVoltage")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputVoltage.u$(slot)0$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"V")
    field(DESC,"Channel output voltage setting")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "3")
}

record(ao, "Mod$(module)-$(device)/outputCurrent")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputCurrent.u$(slot)0$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"A")
    field(DESC,"Channel Current limit set")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "1")
}

record(longout, "Mod$(module)-$(device)/outputTripTimeMaxCurrent")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputTripTimeMaxCurrent.u$(slot)0$(channel) INTEGER: 100 i")
    field(SCAN,"Passive")
    field(EGU,"msec")
    field(DESC,"Channel trip delay on over current")
    field(MDEL,"0")
    field(ADEL,"0")
}

record(longout, "Mod$(module)-$(device)/outputSupervisionBehavior")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionBehavior.u$(slot)0$(channel) INTEGER: 100 i")
    field(SCAN,"Passive")
    field(EGU,"mask")
    field(DESC,"Channel Supervision Behavior")
    field(MDEL,"0")
    field(ADEL,"0")
}

record(stringin, "Mod$(module)-$(device)/outputSwitchStatus")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputSwitch.u$(slot)0$(channel) BITS:__ 100 I")
    field(SCAN,".5 second")
    field(DESC,"Output Switch Status")
}

record(longout, "Mod$(module)-$(device)/outputSwitch")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSwitch.u$(slot)0$(channel) ( 100 i")
    field(SCAN,"Passive")
    field(DESC,"Output Switch Setting")
    field(MDEL,"0")
    field(ADEL,"0")
    field(HIHI,"2")
    field(HIGH,"2")
    field(LOW,"0")
    field(LOLO,"0")
    field(LLSV, MAJOR)
    field(LSV, MINOR)
    field(HSV, MINOR)
    field(HHSV, MAJOR)
}

record(stringin, "Mod$(module)-$(device)/outputStatus")
{
    field(DTYP,"Snmp")
    field(INP,"@$(HOST) $(COMMUNITY) $(W)::outputStatus.u$(slot)0$(channel) BITS:__ 100")
    field(SCAN,".5 second")
    field(DESC,"Output Status")
    field(FLNK,"")
}

record(ao, "Mod$(module)-$(device)/outputVoltageRiseRate")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputVoltageRiseRate.u$(slot)0$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"V/sec")
    field(DESC,"HV Rise Rate")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "3")
}

record(ao, "Mod$(module)-$(device)/outputVoltageFallRate")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputVoltageFallRate.u$(slot)0$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"V/sec")
    field(DESC,"HV Fall Rate")
    field(MDEL,"0")
    field(ADEL,"0")
    field(PREC, "3")
}

record(ao, "Mod$(module)-$(device)/outputSupervisionMaxCurrent")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputConfigMaxCurrent.u$(slot)0$(channel) Float: 100 Fn")
    field(SCAN,"Passive")
    field(EGU,"A")
    field(DESC,"Max Sense Current SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

# Constant nan read errors
# record(ao, "Mod$(module)-$(device)/outputSupervisionMaxSenseVoltage")
# {
#     field(DTYP,"Snmp")
#     field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionMaxSenseVoltage.u$(slot)0$(channel) Float: 100 F")
#     field(SCAN,"Passive")
#     field(EGU,"V")
#     field(DESC,"Max Sense Voltage SW")
#     field(MDEL,"0")
#     field(ADEL,"0")
# }

record(ao, "Mod$(module)-$(device)/outputSupervisionMaxTerminalVoltage")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionMaxTerminalVoltage.u$(slot)0$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"V")
    field(DESC,"Max Terminal Voltage SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

record(ao, "Mod$(module)-$(device)/outputSupervisionMaxPower")
{
    field(DTYP,"Snmp")
    field(OUT,"@$(HOST) $(COMMUNITY) $(W)::outputSupervisionMaxTerminalVoltage.u$(slot)0$(channel) Float: 100 F")
    field(SCAN,"Passive")
    field(EGU,"W")
    field(DESC,"Max Power SW")
    field(MDEL,"0")
    field(ADEL,"0")
}

