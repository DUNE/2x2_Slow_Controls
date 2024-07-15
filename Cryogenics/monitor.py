import psycopg2
from influxdb import InfluxDBClient
import json
import time
import threading
import traceback
from datetime import datetime
import pytz
from configparser import ConfigParser

def make_query(tagid, sensor_info, conn, source_client):
    '''
    Makes SQL query to PostgreSQL database
    '''

    with conn.cursor() as cursor:
        # Generate db name:
        now = datetime.now()
        year_month = now.strftime('%Y_%m')
        table_name = f"sqlt_data_1_{year_month}"

        # Make query
        query = f"""
            SELECT t_stamp, {sensor_info['column']}
            FROM {table_name}
            WHERE tagid = %s
            ORDER BY t_stamp DESC
            LIMIT 1
        """
        cursor.execute(query, (tagid,))  
        timestamp, value = cursor.fetchone()

        # Send to influxDB
        sendToINFLUXDB(timestamp, tagid, value, sensor_info, source_client)

def LAr_O2_XY(conn, source_client):
    '''
    Send data specifically for XY plot between LAr level and oxygen level
    '''
    with conn.cursor() as cursor:
        # Generate db name:
        now = datetime.now()
        year_month = now.strftime('%Y_%m')
        table_name = f"sqlt_data_1_{year_month}"

        # Define tables to read
        datatype = "floatvalue"
        tag1 = "237"
        tag2 = "1223"

        # Make query
        query = f"""
            SELECT t_stamp, {datatype}
            FROM {table_name}
            WHERE tagid = %s
            ORDER BY t_stamp DESC
            LIMIT 1
        """
        cursor.execute(query, (tag1,))  
        timestamp1, value1 = cursor.fetchone()

        cursor.execute(query, (tag2,))  
        timestamp2, value2 = cursor.fetchone()

        timestamp = timestamp1
        '''
        Send data to influxDB
        '''
        # Convert milliseconds to seconds
        timestamp_seconds = timestamp / 1000
        # Create a UTC datetime object
        dt = datetime.fromtimestamp(timestamp_seconds, tz=pytz.UTC)
        # Format the UTC time as a string
        formatted_time = dt.strftime('%Y%m%d %H:%M:%S')

        # Save to influxDB
        datapoint = {
            "measurement" : "LAr_O2_XY",
            "time" : formatted_time,
            "fields" : {
                "O2" : float(value1),
                "LAr" : float(value2),
                "tagid" : tag1+"_"+tag2,
                "description" : "LAr_O2_XY",
                "units" : "ppb_mm"
            }
        }

        # Write data point to InfluxDB
        source_client.write_points([datapoint])

     
    
def sendToINFLUXDB(timestamp, tagid, value, sensor_info, source_client):
    '''
    Send data to influxDB
    '''
    # Convert milliseconds to seconds
    timestamp_seconds = timestamp / 1000
    # Create a UTC datetime object
    dt = datetime.fromtimestamp(timestamp_seconds, tz=pytz.UTC)
    # Format the UTC time as a string
    formatted_time = dt.strftime('%Y%m%d %H:%M:%S')

    # Save to influxDB
    datapoint = {
          "measurement" : sensor_info['name'],
          "time" : formatted_time,
          "fields" : {
               "magnitude" : float(value),
               "tagid" : tagid,
               "description" : sensor_info['description'],
               "units" : sensor_info['units']
          }
     }
    # RTD relative position wrt cryostat calibration
    if sensor_info['name']=="LT-1007A":
         RTD_pos = 0.8145*float(value) - 2158.8
         datapoint["fields"]["Level_meter_RTD_pos"] = RTD_pos

    # Write data point to InfluxDB
    source_client.write_points([datapoint])

def main():
    '''
    Recover PostgreSQL cryo data continuosuly
    '''

    # Reading sensor information
    with open('dictionary.json', 'r') as file:
        sensors = json.load(file)

    configParser = ConfigParser()
    try:
        configParser.read("config.ini")
    except FileNotFoundError:
        configParser.read("/config.ini")
    conf = configParser['secrets']

     # Source InfluxDB connection settings
    source_host = conf['source_host']
    source_port = conf['source_port']

    # Connect to the source InfluxDB instance
    source_client = InfluxDBClient(source_host, source_port, "cryo_readonly")
    source_client.create_database("cryo_readonly")
    source_client.switch_database("cryo_readonly")   

    # Make database connection and query
    try:
        with psycopg2.connect(
            database=conf["database"],
            host=conf["host"],
            user=conf["user"],
            password=conf["password"],
            port=conf["port"]
        ) as conn:
            try:
                while True:
                    for tagid, sensor_info in sensors.items():
                        make_query(tagid, sensor_info, conn, source_client)
                    # Sleep for 1 second
                    time.sleep(1)
                    LAr_O2_XY(conn, source_client)
            except Exception as e:
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                traceback.print_exc()
        main()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
     

if __name__ == "__main__":
    threading.Thread(target=main).start()
 



   