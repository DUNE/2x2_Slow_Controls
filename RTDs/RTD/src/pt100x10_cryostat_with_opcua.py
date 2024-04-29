#!/usr/bin/python
import time, math, json
import subprocess
import asyncio
from configparser import ConfigParser

from asyncua import Server, ua
import socket

async def main():
    import max31865
    
    conf = ConfigParser()
    conf.read("/home/pi/Dune2x2_SlowControl/config.ini")

    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]

    #Read device IP
    ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ips.connect((db["PINGIP"], 80))
    ip = ips.getsockname()[0]
    ips.close()


    #Setup OPC UA server
    s = Server()
    await s.init()
    opc_port = "4841"
    s.set_endpoint("opc.tcp://"+ip+":"+opc_port)
    idx = await s.register_namespace("http://"+ip+":"+opc_port)
    uaobj = await s.nodes.objects.add_object(idx,db["OPCSERVERNAME"])
    uavar = []
    for i, sens in enumerate(json.loads(para["RTD_SENS_LIST"])):
        uavar.append(await uaobj.add_variable(idx,"sens%02d" % sens,273.15))
        await uavar[i].set_writable()


    misoPin = 9
    mosiPin = 10
    clkPin  = 11

    cs0Pin = 26
    cs1Pin = 19
    cs2Pin = 13
    cs3Pin = 0o6
    cs4Pin = 0o5
    cs5Pin = 27
    cs6Pin = 17
    cs7Pin = 0o4
    cs8Pin = 0o3
    cs9Pin = 0o2

    sens0 = max31865.max31865(cs0Pin,misoPin,mosiPin,clkPin)
    sens1 = max31865.max31865(cs1Pin,misoPin,mosiPin,clkPin)
    sens2 = max31865.max31865(cs2Pin,misoPin,mosiPin,clkPin)
    sens3 = max31865.max31865(cs3Pin,misoPin,mosiPin,clkPin)
    sens4 = max31865.max31865(cs4Pin,misoPin,mosiPin,clkPin)
    sens5 = max31865.max31865(cs5Pin,misoPin,mosiPin,clkPin)
    sens6 = max31865.max31865(cs6Pin,misoPin,mosiPin,clkPin)
    sens7 = max31865.max31865(cs7Pin,misoPin,mosiPin,clkPin)
    sens8 = max31865.max31865(cs8Pin,misoPin,mosiPin,clkPin)
    sens9 = max31865.max31865(cs9Pin,misoPin,mosiPin,clkPin)

    async with s:
        while True:
            await asyncio.sleep(int(para["CTIME"]))
            for i, sens in enumerate(json.loads(para["RTD_SENS_LIST"])):
                temp_C = eval('sens'+str(sens)+'.readTemp()')
                print("sens%d: %f degC\n" % (sens,temp_C))
                post = "temp,sens=" + str(sens) + ",pos=" + str(meta["POS"]) + " value=" + str(temp_C)
                subprocess.call(["curl", "-i", "-XPOST", db["URL"]+":"+str(db["PORT"])+"/write?db="+db["NAME"], "--data-binary", post])
                await uavar[i].write_value(temp_C+273.15)

if __name__ == "__main__":
    asyncio.run(main(), debug=True)