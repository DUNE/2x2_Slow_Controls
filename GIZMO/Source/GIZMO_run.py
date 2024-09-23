import json
from GIZMO_library import GIZMO
import threading

# Reading other units JSON file
with open('CONFIG/others_units.json', "r") as json_file:
    othersDB = json.load(json_file)

# Get list of units not attached to modules
id = 0
others_dict = {}
# Get list of units not attached to modules
for unit in othersDB.keys():
    kind = othersDB[unit]["class"]
    others_dict[id] = GIZMO(None, unit, othersDB[unit])
    id += 1

# Continuous monitoring
threading.Thread(target=others_dict[0].CONTINUOUS_monitoring, args=([]), kwargs={}).start()
