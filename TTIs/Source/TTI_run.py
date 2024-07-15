import json
from TTI_library import TTI
import threading

moduleDB = {}
for i in range(4): 
    file_path = f'CONFIG/module{i}.json'
    with open(file_path, "r") as json_file:
        moduleDB.update(json.load(json_file))

# Get list of units attached to modules
id = 0
attached_units_dict = {}
for module in moduleDB.keys():
    unit_names = moduleDB[module].keys()
    for unit in unit_names:
        kind = moduleDB[module][unit]["class"]
        attached_units_dict[id] = TTI(module, unit, moduleDB[module][unit])
        id += 1 

# Continuous monitoring
for tti in range(id):
    threading.Thread(target=attached_units_dict[tti].CONTINUOUS_monitoring, args=(["voltage"]), kwargs={}).start()
