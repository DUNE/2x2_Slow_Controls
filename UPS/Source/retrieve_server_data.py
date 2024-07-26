import asyncio
from asyncua import Client
from utils import parse_config
import os


async def get_variable(obj,var_name):
    '''Function to retrieve a variable
    from a node object 

    Parameters:
    ----------

    obj: asyncua node object
         Object containing the variables

    var_name: string
         Name of the variable that 
         will be retrieved from the server

    Returns:
    --------

    var_val: string
            Current value of
            the variable 
    '''
    # Get a variable node
    myvar = await obj.get_child([f"2:{var_name}"])
    # Read the value of the variable
    var_val = await myvar.read_value()
    return var_val 


async def retrieve_data():
    '''
    Function used to
    retrieve data from an OPC
    sever using asyncua
    '''
    cfg = os.getenv('TOP_DIR') +"/config/UPS.cfg"
    input_par = parse_config(cfg)
    IP = input_par['raspi_ip']
    PORT = input_par['port']
    url=f"opc.tcp://{IP}:{PORT}/freeopcua/server/"
    # Create a client instance
    async with Client(url) as client:
        print("Connected to the server")
        # Get the root node
        root = client.nodes.root
        # Browse the root node
        objects = await root.get_child(["0:Objects"])
        # Browse for a specific object/node
        myobj = await objects.get_child(["2:UPSSet"])
        print("Current date is: ", await get_variable(
            myobj,
            "DateVar"
        ))
        print("Battery Failing? ", await get_variable(
            myobj,
            "BatFail"
        ))
        print("Remaining battery time: ", await get_variable(
            myobj,
            "BatTime"
        ))
        print("Battery capacity: ", await get_variable(
            myobj,
            "BatCap"
        ))
        print("Battery voltage: ", await get_variable(
            myobj,
            "BatV"
        ))
        print("Battery age: ", await get_variable(
            myobj,
            "BatAge"
        ))
        
    

# Run the client script
if __name__ == "__main__":
    asyncio.run(retrieve_data())

