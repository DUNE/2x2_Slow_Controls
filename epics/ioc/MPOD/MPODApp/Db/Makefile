TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
# Create and install (or just install) into <top>/db
# databases, templates, substitutions like this

DB += crate.db
DB += slot_slot0.db
DB += slot_slot1-3.db
DB += channel_slot0.tpl
DB += channel_slot1-3.tpl
DB += VGA_Mod0.sub
DB += VGA_Mod1.sub
DB += VGA_Mod2.sub
DB += VGA_Mod3.sub
DB += RTD_Mod0.sub
DB += RTD_Mod1.sub
DB += RTD_Mod2.sub
DB += RTD_Mod3.sub
DB += PAC_Mod0.sub
DB += PAC_Mod1.sub
DB += PAC_Mod2.sub
DB += PAC_Mod3.sub

#----------------------------------------------------
# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_template = <templatename>

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

