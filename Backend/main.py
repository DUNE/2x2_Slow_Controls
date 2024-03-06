#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FAST API PACKAGES
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# INTERNAL MANAGEMENT CLASSES
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# Remove app. if running it out of the docker container
from app.CLASSES.MPOD_library import MPOD
from app.CLASSES.MPOD_library import UNIT
from app.CLASSES.dictionary import classes_dictionary
import json
import threading
import os

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# GENERATING OBJECT MODELS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# Reading modules JSON file
moduleDB = {}
for i in range(4): # JUST MODULE 0 FOR NOW
    file_path = f'app/CONFIG/module{i}.json'
    with open(file_path, "r") as json_file:
        moduleDB.update(json.load(json_file))

# Reading other units JSON file
with open('app/CONFIG/others_units.json', "r") as json_file:
    othersDB = json.load(json_file)

# Get list of units  attached to modules
id = 0
attached_units_dict = {}
attached_units_dict2 = {}
for module in moduleDB.keys():
    unit_names = moduleDB[module].keys()
    for unit in unit_names:
        kind = moduleDB[module][unit]["class"]
        object = classes_dictionary[kind]
        attached_units_dict[id] = object(module, unit, moduleDB[module][unit])
        attached_units_dict2[module] = {id : attached_units_dict[id]}
        id += 1 

id = 0
others_dict = {}
# Get list of units not attached to modules
for unit in othersDB.keys():
    kind = othersDB[unit]["class"]
    object = classes_dictionary[kind]
    others_dict[id] = object(None, unit, othersDB[unit])
    id += 1

# REMOTE MONITORING FOR GIZMO
threading.Thread(target=others_dict[1].CONTINUOUS_monitoring, args=(), kwargs={}).start()

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FAST API CONFIGURATION
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FastAPI handles JSON serialization and deserialization for us.
description = """
SlowControlsApp allows you to manage the units connected (and not) to each module.

## CRUD (Create, Read, Update, Delete)
Because all we want to do is manage (turn stuff ON/OFF), we will only use Read and Update methods. Remember that each module configuration (units connected, channels, powering, etc.) is stored in a single JSON file located on /CONFIG/modules_units.json. We also have units (such as gizmo) that are not connected to each of the modules but that we also track and manage, we call them 'others'. The configuration for these units can be found on /CONFIG/other_units.json.
"""
tags_metadata = [
{
"name" : "Read",
"description" :
"""
* **Read modules' JSON configuration file** (_get raw JSON file_)
* **Read others' JSON configuration file** (_get raw JSON file_)
* **Read units connected to modules** (_get dictionary with attached units objects with unique id_)
* **Read unit connected to module by ID** (_get configuration dictionary of specific unit_)
* **Read other units** (_get dictionary with other units objects with unique id_)
* **Read other unit by ID** (_get configuration dictionary of specific unit_)
* **Read status of unit connected to module by ID** (_get boolean response if unit is ON/OFF_)
* **Read status of other unit by ID** (_get boolean response if unit is ON/OFF_)
"""
},
{
"name" : "Update",
"description" :
"""
* **Turn ON unit connected to module by unit ID** (_get success response and measure output continuously_)
* **Turn OFF unit connected to module by unit ID** (_get success response and measure output continuously_)
* **Turn ON other unit by unit ID** (_get success response_)
* **Turn OFF other unit by unit ID** (_get success response_)
"""
}
]

app = FastAPI(
    title = "SlowControlsApp",
    description = description,
    summary = "API manager for Mx2 slow control components such as gizmo, TTI, mpod, etc.",
    version = "0.0.1",
    openapi_tags=tags_metadata,
    contact={
        "name" : "Renzo Vizarreta",
        "email" : "rvizarr@fnal.gov",
    }
)

# Adding cors headers
from fastapi.middleware.cors import CORSMiddleware
# Adding cors urls
origins = [
    'http://192.168.197.46:3006', # PRODUCTION REACT APP
    'http://192.168.197.46:3002', # TEST REACT APP
]
# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# CRUD API FUNCTIONALITY
# Create, Read, Update, Delete
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# GET METHODS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
@app.get("/")
def index():
    return {"message" : "Hello World!"}

@app.get("/allmodules", tags=["Read"])
def get_ModulesJSON():
    '''
    Return modules JSON file
    '''
    return moduleDB

@app.get("/allothers", tags=["Read"])
def get_other_modulesJSON():
    '''
    Return other units (i.e. Gizmo) JSON file
    '''
    return othersDB

@app.get("/attached_units", tags=["Read"])
def get_attached_units():
    '''
    Return all objects of units connected to modules
    '''
    return attached_units_dict

@app.get("/attached_units2", tags=["Read"])
def get_attached_units2():
    '''
    Return all objects of units connected to modules
    '''
    return attached_units_dict2


@app.get("/attached_units/{unit_id}", tags=["Read"])
def get_attached_unit_by_id(unit_id: int):
    '''
    Return object by id
    '''
    return attached_units_dict[unit_id]

@app.get("/other_units", tags=["Read"])
def get_other_units():
    '''
    Return all objects of units NOT connected to modules
    '''
    return others_dict

@app.get("/other_units/{unit_id}", tags=["Read"])
def get_others_by_id(unit_id: int):
    '''
    Return object by id
    '''
    return others_dict[unit_id]

@app.get("/attached_units/{unit_id}/status", tags=["Read"])
def get_attached_status_by_id(unit_id: int):
    '''
    Return unit status of measuring elements (i.e. {light, current, rtd})
    '''
    return attached_units_dict[unit_id].getMeasuringStatus()

@app.get("/attached_units/{unit_id}/crate_status", tags=["Read"])
def get_attached_crate_status_by_id(unit_id: int):
    '''
    Return unit crate status 
    '''
    return attached_units_dict[unit_id].getCrateStatus()

@app.get("/other_units/{unit_id}/status", tags=["Read"])
def get_other_status_by_id(unit_id: int):
    '''
    Return other unit status (i.e. MPOD crate status)
    '''
    return others_dict[unit_id].getCrateStatus()
    
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# PUT METHODS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
import time
@app.put("/attached_units/{unit_id}/{measuring}/turn-on", tags=["Update"])
async def turnON_attached_by_id(unit_id: int, measuring: str):
    '''
    Turn on ALL CHANNELS of measuring from unit connected to module (i.e. light readout from MPOD)
    '''
    attached_units_dict[unit_id].powerON(measuring) 
    # Continuous monitoring
    threading.Thread(target=attached_units_dict[unit_id].CONTINUOUS_monitoring, args=([measuring]), kwargs={}).start()
    if attached_units_dict[unit_id].getClass() == "TTI":
        threading.Thread(target=attached_units_dict[unit_id].ramp_up(100,1), args=([measuring]), kwargs={}).start()
    return {"message" : attached_units_dict[unit_id].getOnMessage() + " Measuring: " + measuring} 

@app.put("/attached_units/{unit_id}/{measuring}/{channel}/turn-on", tags=["Update"])
async def turnON_single_channel(unit_id: int, measuring: str, channel: str):
    '''
    Turn on SINGLE CHANNEL of measuring from unit connected to module (i.e. Pacman 1 of charge readout from MPOD)
    '''
    attached_units_dict[unit_id].powerON_channel(measuring, channel) 
    # Continuous monitoring (TBD)
    threading.Thread(target=attached_units_dict[unit_id].CONTINUOUS_monitoring, args=([measuring]), kwargs={}).start()
    if attached_units_dict[unit_id].getClass() == "TTI":
        threading.Thread(target=attached_units_dict[unit_id].ramp_up(100,1), args=([measuring]), kwargs={}).start()
    return {"message" : attached_units_dict[unit_id].getOnMessage() + ". Measuring: " + measuring + ", channel: " + channel} 

#loop.create_task(turnON_attached_by_id)

@app.put("/attached_units/{unit_id}/{measuring}/turn-off", tags=["Update"])
def turnOFF_attached_by_id(unit_id: int, measuring: str):
    '''
    Turn off measuring from unit connected to module (i.e. light readout from MPOD)
    '''
    attached_units_dict[unit_id].powerOFF(measuring)
    return {"message" : attached_units_dict[unit_id].getOffMessage()} 

@app.put("/attached_units/{unit_id}/{measuring}/{channel}/turn-off", tags=["Update"])
def turnOFF_attached_by_id(unit_id: int, measuring: str, channel : str):
    '''
    Turn off SINGLE CHANNEL of measuring from unit connected to module (i.e. Pacman 1 of charge readout from MPOD)
    '''
    attached_units_dict[unit_id].powerOFF_channel(measuring, channel)
    return {"message" : attached_units_dict[unit_id].getOffMessage()+ ". Measuring: " + measuring + ", channel: " + channel} 

@app.put("/other_units/{unit_id}/turn-on", tags=["Update"])
def turnON_other_by_id(unit_id: int):
    '''
    Turn on unit NOT connected to module (i.e. MPOD Crate)
    '''
    # REMOTE MONITORING FOR MPOD CRATE
    others_dict[unit_id].powerSwitch(1)
    if others_dict[unit_id].getClass() != "GIZMO":
        modules = others_dict[unit_id].getModules()
        for module in modules:
            for id in attached_units_dict2[module].keys():
                attached_units_dict2[module][id].powerSwitch(1)

    # This will raise an error for the mpod crate!
    return {"message" : others_dict[unit_id].getOnMessage()} 


@app.put("/other_units/{unit_id}/turn-off", tags=["Update"])
def turnOFF_other_by_id(unit_id: int):
    '''
    Turn off unit NOT connected to module (i.e. MPOD Crate)
    '''
    others_dict[unit_id].powerSwitch(0)
    modules = others_dict[unit_id].getModules()
    for module in modules:
        for id in attached_units_dict2[module].keys():
            attached_units_dict2[module][id].powerSwitch(0)
    return {"message" : others_dict[unit_id].getOffMessage()} 
