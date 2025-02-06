from obspy import read, UTCDateTime
import numpy as np
import paho.mqtt.client as mqtt
import ssl
import configparser
import io 
import os
import logging 
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# Read the configuration file and load env variables 
config_path = "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

load_dotenv()

# Create a new InfluxDB client
influx_client = InfluxDBClient(url = os.getenv("URL"), token=os.getenv("TOKEN"), org=os.getenv("ORG"))

logging.getLogger().setLevel(logging.INFO)


# Set up logging errors
logging.basicConfig(filename='src/logs/errors.log', level=logging.ERROR)

# Function to process MiniSEED files and write to InfluxDB
def mseed2influxdb(data, axis, timens, sensor_id):
    byte_io = io.BytesIO(data) # Create a BytesIO object from the data 
    try: # If some files/bytes are corrupted, the program will ignore them and continue with the next ones
        st = read(byte_io, format = "MSEED")
        trace = st[0] # There is only one trace in the Stream object
    except Exception as e:
        print(f"Error reading file at timestamp: {timens}: {e}")
        logging.error(f"Error reading file at timestamp: {timens}: {e}")
        return
    
    # List of Points
    points = [Point("acceleration")
              .tag("sensor_id", sensor_id)
              .field(axis, value)
              .time((trace.stats.starttime + i * trace.stats.delta).isoformat())
              for i, value in enumerate(trace.data)]
    # Write the points to InfluxDB
    with influx_client.write_api(write_options=SYNCHRONOUS) as write_api:
        write_api.write(bucket = os.getenv("BUCKET"), record=points)
        #print(trace)
        print(f"Finished writing file/bytes from {sensor_id}_{axis} at timestamp: {timens}")

# Function to process temperature data and write to InfluxDB
def temperature2influxdb(temperature, timens, sensor_id):
    point = Point("temperature").tag("sensor_id", sensor_id).field("temperature", temperature).time(UTCDateTime(timens*1e-9).isoformat())
    with influx_client.write_api(write_options=SYNCHRONOUS) as write_api:
        write_api.write(bucket = os.getenv("BUCKET"), record=point)
        print(f"Finished writing temperature data from {sensor_id} at timestamp: {timens}\n")

# Callback for MQTT messages
def on_message(mqtt_client, userdata, msg):
    
    # Convert the MQTT payload into a byte array
    bytes_array = msg.payload
    # Encoding (uint16) is represented by bytes 0...3
    encoding = int.from_bytes(bytes_array[0:1], byteorder='little')
    # index (uint16) is represented by bytes 4...7
    index = int.from_bytes(bytes_array[1:2], byteorder='little')
    # timestamp (uint64) is represented by bytes 8...15
    timens = int.from_bytes(bytes_array[8:16], byteorder='little')
    # index (uint16) is represented by bytes 16...17
    samples = int.from_bytes(bytes_array[16:18], byteorder='little')
    # size_x (uint16) is represented by bytes 18...19
    size_x = int.from_bytes(bytes_array[18:20], byteorder='little')
    # size_y (uint16) is represented by bytes 20...21
    size_y = int.from_bytes(bytes_array[20:22], byteorder='little')
    # size_z (uint16) is represented by bytes 22...23
    size_z = int.from_bytes(bytes_array[22:24], byteorder='little')
    # temperature (float32) is represented by bytes 24...27
    temperature = np.frombuffer(bytes_array[24:28], dtype=np.float32)[0]


    # Extract size_x bytes starting from position 28
    data_x = bytes_array[28:28 + size_x]
    # Extract size_y bytes starting from the position after data_x
    data_y = bytes_array[28 + size_x: 28 + size_x + size_y]
    # Extract size_z bytes starting from the position after data_y
    data_z = bytes_array[28 + size_x + size_y: 28 + size_x + size_y + size_z]
    
    
    # Extract sensor_id from a MSEED stream
    sensor_id = read(io.BytesIO(data_z), format="MSEED")[0].id
    #print(sensor_id)
    # Extract the list of sensors from the config file 
    sensors_list = config['sensors']['sensors'].replace(" ", "").replace("\n", "").split(",")

    # Generate packets only if the sensor_id is in the list of allowed sensors
    if sensor_id in sensors_list:
        if size_x > 0 :
            mseed2influxdb(data_x, 'x', timens, sensor_id)
        if size_y > 0 :
            mseed2influxdb(data_y, 'y', timens, sensor_id)
        if size_z > 0 :
            mseed2influxdb(data_z, 'z', timens, sensor_id)
        if config['sensors'].getboolean('use_temperature'):
            temperature2influxdb(temperature, timens, sensor_id)

    # print all information about mqtt received packet
    # print("encoding: " + str(encoding))
    # print("index: " + str(index))
    # print("samples: " + str(samples))
    # print("size_x: " + str(size_x))
    # print("size_y: " + str(size_y))
    # print("size_z: " + str(size_z))
    # print("temprature: " + str(temperature))

# Callback for MQTT connection
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
    # subscribe to the S.H.M. topic with QOS 1
	client.subscribe(config['MQTT']['topic'], config.getint('MQTT','qos'))

# Callback for MQTT subscription
def on_subscribe(client, userdata, mid, granted_qos):
    # client is subscribed
	print("Subscribed: " + str(mid) + " " + str(granted_qos))



def main():
    # Connect to broker
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe

    mqtt_client.tls_set(ca_certs = config['TLS']['ca_cert'], 
                certfile = config['TLS']['client_cert'], 
                keyfile = config['TLS']['client_key'], 
                cert_reqs=ssl.CERT_REQUIRED)
    
    mqtt_client.tls_insecure_set(True)

    print("Broker IP: " + config['MQTT']['broker'])
    mqtt_client.connect(config['MQTT']['broker'], config.getint('MQTT','port'), 60)
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()